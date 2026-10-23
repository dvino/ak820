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
      000685                        596 _D0SetupReqCode::
      000685                        597 	.ds 1
      000686                        598 _D0SetupLen::
      000686                        599 	.ds 2
      000688                        600 _pD0Descr::
      000688                        601 	.ds 3
      00068B                        602 _D0UsbConfig::
      00068B                        603 	.ds 1
      00068C                        604 _USB_EnumStatus::
      00068C                        605 	.ds 1
      00068D                        606 _USB_SleepStatus::
      00068D                        607 	.ds 1
      00068E                        608 _MCU_Sleep_Operate::
      00068E                        609 	.ds 1
      00068F                        610 _KB_USB_UpStatus::
      00068F                        611 	.ds 1
      000690                        612 _KB_USB_SetReport::
      000690                        613 	.ds 1
      000691                        614 _ak820_boot_stage::
      000691                        615 	.ds 1
      000692                        616 _ak820_main_heartbeat::
      000692                        617 	.ds 1
      000693                        618 _raw_state:
      000693                        619 	.ds 1
      000694                        620 _raw_buffer:
      000694                        621 	.ds 32
      0006B4                        622 _raw_reply_without_nvm:
      0006B4                        623 	.ds 1
      0006B5                        624 _keyboard_reset:
      0006B5                        625 	.ds 1
      0006B6                        626 _input_snapshot:
      0006B6                        627 	.ds 46
      0006E4                        628 _control_phase:
      0006E4                        629 	.ds 1
      0006E5                        630 _output_kind:
      0006E5                        631 	.ds 1
      0006E6                        632 _output_report_id:
      0006E6                        633 	.ds 1
      0006E7                        634 _control_zlp:
      0006E7                        635 	.ds 1
      0006E8                        636 _control_pointer:
      0006E8                        637 	.ds 2
      0006EA                        638 _descriptor_select_PARM_2:
      0006EA                        639 	.ds 1
      0006EB                        640 _descriptor_select_PARM_3:
      0006EB                        641 	.ds 2
      0006ED                        642 _descriptor_select_type_10000_265:
      0006ED                        643 	.ds 1
      0006EE                        644 _control_setup_length_10000_286:
      0006EE                        645 	.ds 2
      0006F0                        646 _control_setup_offset_10000_286:
      0006F0                        647 	.ds 1
      0006F1                        648 _ak820_usb_send_PARM_2:
      0006F1                        649 	.ds 2
      0006F3                        650 _ak820_usb_send_PARM_3:
      0006F3                        651 	.ds 1
      0006F4                        652 _ak820_usb_send_endpoint_10000_412:
      0006F4                        653 	.ds 1
      0006F5                        654 _ak820_usb_send_offset_10000_413:
      0006F5                        655 	.ds 1
      0006F6                        656 _ak820_usb_try_send_PARM_2:
      0006F6                        657 	.ds 2
      0006F8                        658 _ak820_usb_try_send_PARM_3:
      0006F8                        659 	.ds 1
      0006F9                        660 _ak820_usb_try_send_endpoint_10000_433:
      0006F9                        661 	.ds 1
      0006FA                        662 _ak820_usb_try_send_sent_10000_434:
      0006FA                        663 	.ds 1
      0006FB                        664 _ak820_usb_raw_send_PARM_2:
      0006FB                        665 	.ds 1
      0006FC                        666 _ak820_usb_raw_send_report_10000_449:
      0006FC                        667 	.ds 3
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
      0053E1                        719 _raw_abort:
                                    720 ;	tmk_core/protocol/ch555/usb_ak820.c:87: if (raw_state == RAW_WORK || raw_state == RAW_TX_ACTIVE ||
      0053E1 90 06 93         [24]  721 	mov	dptr,#_raw_state
      0053E4 E0               [24]  722 	movx	a,@dptr
      0053E5 FF               [12]  723 	mov	r7,a
      0053E6 BF 03 02         [24]  724 	cjne	r7,#0x03,00130$
      0053E9 80 1C            [24]  725 	sjmp	00101$
      0053EB                        726 00130$:
      0053EB 90 06 93         [24]  727 	mov	dptr,#_raw_state
      0053EE E0               [24]  728 	movx	a,@dptr
      0053EF FF               [12]  729 	mov	r7,a
      0053F0 BF 04 02         [24]  730 	cjne	r7,#0x04,00131$
      0053F3 80 12            [24]  731 	sjmp	00101$
      0053F5                        732 00131$:
                                    733 ;	tmk_core/protocol/ch555/usb_ak820.c:88: raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED)
      0053F5 90 06 93         [24]  734 	mov	dptr,#_raw_state
      0053F8 E0               [24]  735 	movx	a,@dptr
      0053F9 FF               [12]  736 	mov	r7,a
      0053FA BF 06 02         [24]  737 	cjne	r7,#0x06,00132$
      0053FD 80 08            [24]  738 	sjmp	00101$
      0053FF                        739 00132$:
      0053FF 90 06 93         [24]  740 	mov	dptr,#_raw_state
      005402 E0               [24]  741 	movx	a,@dptr
      005403 FF               [12]  742 	mov	r7,a
      005404 BF 07 08         [24]  743 	cjne	r7,#0x07,00102$
      005407                        744 00101$:
                                    745 ;	tmk_core/protocol/ch555/usb_ak820.c:89: raw_state = RAW_CANCELLED;
      005407 90 06 93         [24]  746 	mov	dptr,#_raw_state
      00540A 74 07            [12]  747 	mov	a,#0x07
      00540C F0               [24]  748 	movx	@dptr,a
      00540D 80 05            [24]  749 	sjmp	00103$
      00540F                        750 00102$:
                                    751 ;	tmk_core/protocol/ch555/usb_ak820.c:91: raw_state = RAW_IDLE;
      00540F 90 06 93         [24]  752 	mov	dptr,#_raw_state
      005412 E4               [12]  753 	clr	a
      005413 F0               [24]  754 	movx	@dptr,a
      005414                        755 00103$:
                                    756 ;	tmk_core/protocol/ch555/usb_ak820.c:92: output_kind = OUTPUT_NONE;
      005414 90 06 E5         [24]  757 	mov	dptr,#_output_kind
      005417 E4               [12]  758 	clr	a
      005418 F0               [24]  759 	movx	@dptr,a
                                    760 ;	tmk_core/protocol/ch555/usb_ak820.c:93: }
      005419 22               [24]  761 	ret
                                    762 ;------------------------------------------------------------
                                    763 ;Allocation info for local variables in function 'raw_complete'
                                    764 ;------------------------------------------------------------
                                    765 ;	tmk_core/protocol/ch555/usb_ak820.c:95: static void raw_complete(void) {
                                    766 ;	-----------------------------------------
                                    767 ;	 function raw_complete
                                    768 ;	-----------------------------------------
      00541A                        769 _raw_complete:
                                    770 ;	tmk_core/protocol/ch555/usb_ak820.c:96: if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_DRAINED;
      00541A 90 06 93         [24]  771 	mov	dptr,#_raw_state
      00541D E0               [24]  772 	movx	a,@dptr
      00541E FF               [12]  773 	mov	r7,a
      00541F BF 04 07         [24]  774 	cjne	r7,#0x04,00104$
      005422 90 06 93         [24]  775 	mov	dptr,#_raw_state
      005425 74 06            [12]  776 	mov	a,#0x06
      005427 F0               [24]  777 	movx	@dptr,a
      005428 22               [24]  778 	ret
      005429                        779 00104$:
                                    780 ;	tmk_core/protocol/ch555/usb_ak820.c:97: else if (raw_state == RAW_TX_WAIT) raw_state = RAW_IDLE;
      005429 90 06 93         [24]  781 	mov	dptr,#_raw_state
      00542C E0               [24]  782 	movx	a,@dptr
      00542D FF               [12]  783 	mov	r7,a
      00542E BF 05 05         [24]  784 	cjne	r7,#0x05,00106$
      005431 90 06 93         [24]  785 	mov	dptr,#_raw_state
      005434 E4               [12]  786 	clr	a
      005435 F0               [24]  787 	movx	@dptr,a
      005436                        788 00106$:
                                    789 ;	tmk_core/protocol/ch555/usb_ak820.c:98: }
      005436 22               [24]  790 	ret
                                    791 ;------------------------------------------------------------
                                    792 ;Allocation info for local variables in function 'endpoints_reset'
                                    793 ;------------------------------------------------------------
                                    794 ;i             Allocated with name '_endpoints_reset_i_10000_255'
                                    795 ;------------------------------------------------------------
                                    796 ;	tmk_core/protocol/ch555/usb_ak820.c:100: static void endpoints_reset(void) {
                                    797 ;	-----------------------------------------
                                    798 ;	 function endpoints_reset
                                    799 ;	-----------------------------------------
      005437                        800 _endpoints_reset:
                                    801 ;	tmk_core/protocol/ch555/usb_ak820.c:103: D0_EP_MOD = bUX_DEV_EN;
      005437 90 22 0C         [24]  802 	mov	dptr,#0x220c
      00543A 74 01            [12]  803 	mov	a,#0x01
      00543C F0               [24]  804 	movx	@dptr,a
                                    805 ;	tmk_core/protocol/ch555/usb_ak820.c:104: D0_EP1RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      00543D F5 82            [12]  806 	mov	dpl,a
      00543F 74 12            [12]  807 	mov	a,#0x12
      005441 F0               [24]  808 	movx	@dptr,a
                                    809 ;	tmk_core/protocol/ch555/usb_ak820.c:105: D0_EP2RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      005442 A3               [24]  810 	inc	dptr
      005443 F0               [24]  811 	movx	@dptr,a
                                    812 ;	tmk_core/protocol/ch555/usb_ak820.c:106: D0_EP3RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      005444 A3               [24]  813 	inc	dptr
      005445 F0               [24]  814 	movx	@dptr,a
                                    815 ;	tmk_core/protocol/ch555/usb_ak820.c:107: D0_EP1T_L = D0_EP2T_L = D0_EP3T_L = 0;
      005446 90 22 0B         [24]  816 	mov	dptr,#0x220b
      005449 E4               [12]  817 	clr	a
      00544A F0               [24]  818 	movx	@dptr,a
      00544B 15 82            [12]  819 	dec	dpl
      00544D F0               [24]  820 	movx	@dptr,a
      00544E 15 82            [12]  821 	dec	dpl
      005450 F0               [24]  822 	movx	@dptr,a
                                    823 ;	tmk_core/protocol/ch555/usb_ak820.c:108: for (i = 0; i < SNAPSHOT_SIZE; ++i) input_snapshot[i] = 0;
      005451 FF               [12]  824 	mov	r7,a
      005452                        825 00103$:
      005452 EF               [12]  826 	mov	a,r7
      005453 24 B6            [12]  827 	add	a, #_input_snapshot
      005455 F5 82            [12]  828 	mov	dpl,a
      005457 E4               [12]  829 	clr	a
      005458 34 06            [12]  830 	addc	a, #(_input_snapshot >> 8)
      00545A F5 83            [12]  831 	mov	dph,a
      00545C E4               [12]  832 	clr	a
      00545D F0               [24]  833 	movx	@dptr,a
      00545E 0F               [12]  834 	inc	r7
      00545F BF 2E 00         [24]  835 	cjne	r7,#0x2e,00139$
      005462                        836 00139$:
      005462 40 EE            [24]  837 	jc	00103$
                                    838 ;	tmk_core/protocol/ch555/usb_ak820.c:109: input_snapshot[SNAPSHOT_NKRO] = REPORT_ID_NKRO;
      005464 90 06 BE         [24]  839 	mov	dptr,#(_input_snapshot + 0x0008)
      005467 74 06            [12]  840 	mov	a,#0x06
      005469 F0               [24]  841 	movx	@dptr,a
                                    842 ;	tmk_core/protocol/ch555/usb_ak820.c:113: input_snapshot[SNAPSHOT_SYSTEM] = REPORT_ID_SYSTEM;
      00546A 90 06 DE         [24]  843 	mov	dptr,#(_input_snapshot + 0x0028)
      00546D 03               [12]  844 	rr	a
      00546E F0               [24]  845 	movx	@dptr,a
                                    846 ;	tmk_core/protocol/ch555/usb_ak820.c:114: input_snapshot[SNAPSHOT_CONSUMER] = REPORT_ID_CONSUMER;
      00546F 90 06 E1         [24]  847 	mov	dptr,#(_input_snapshot + 0x002b)
      005472 04               [12]  848 	inc	a
      005473 F0               [24]  849 	movx	@dptr,a
                                    850 ;	tmk_core/protocol/ch555/usb_ak820.c:115: for (i = 0; i < RAW_EPSIZE; ++i) pUSB_BUF_DEV0[UX_EP3_ADDR + i] = 0;
      005474 7F 00            [12]  851 	mov	r7,#0x00
      005476                        852 00105$:
      005476 8F 06            [24]  853 	mov	ar6,r7
      005478 74 C0            [12]  854 	mov	a,#0xc0
      00547A 2E               [12]  855 	add	a, r6
      00547B F5 82            [12]  856 	mov	dpl,a
      00547D 74 10            [12]  857 	mov	a,#0x10
      00547F 24 00            [12]  858 	add	a, #0x00
      005481 F5 83            [12]  859 	mov	dph,a
      005483 E4               [12]  860 	clr	a
      005484 F0               [24]  861 	movx	@dptr,a
      005485 0F               [12]  862 	inc	r7
      005486 BF 20 00         [24]  863 	cjne	r7,#0x20,00141$
      005489                        864 00141$:
      005489 40 EB            [24]  865 	jc	00105$
                                    866 ;	tmk_core/protocol/ch555/usb_ak820.c:116: raw_abort();
                                    867 ;	tmk_core/protocol/ch555/usb_ak820.c:117: }
      00548B 02 53 E1         [24]  868 	ljmp	_raw_abort
                                    869 ;------------------------------------------------------------
                                    870 ;Allocation info for local variables in function 'control_stall'
                                    871 ;------------------------------------------------------------
                                    872 ;	tmk_core/protocol/ch555/usb_ak820.c:119: static void control_stall(void) {
                                    873 ;	-----------------------------------------
                                    874 ;	 function control_stall
                                    875 ;	-----------------------------------------
      00548E                        876 _control_stall:
                                    877 ;	tmk_core/protocol/ch555/usb_ak820.c:120: if (raw_state == RAW_RX) raw_state = RAW_IDLE;
      00548E 90 06 93         [24]  878 	mov	dptr,#_raw_state
      005491 E0               [24]  879 	movx	a,@dptr
      005492 FF               [12]  880 	mov	r7,a
      005493 BF 01 05         [24]  881 	cjne	r7,#0x01,00102$
      005496 90 06 93         [24]  882 	mov	dptr,#_raw_state
      005499 E4               [12]  883 	clr	a
      00549A F0               [24]  884 	movx	@dptr,a
      00549B                        885 00102$:
                                    886 ;	tmk_core/protocol/ch555/usb_ak820.c:121: output_kind = OUTPUT_NONE;
      00549B 90 06 E5         [24]  887 	mov	dptr,#_output_kind
      00549E E4               [12]  888 	clr	a
      00549F F0               [24]  889 	movx	@dptr,a
                                    890 ;	tmk_core/protocol/ch555/usb_ak820.c:122: control_phase = CTRL_IDLE;
      0054A0 90 06 E4         [24]  891 	mov	dptr,#_control_phase
      0054A3 F0               [24]  892 	movx	@dptr,a
                                    893 ;	tmk_core/protocol/ch555/usb_ak820.c:123: D0SetupReqCode = 0xff;
      0054A4 90 06 85         [24]  894 	mov	dptr,#_D0SetupReqCode
      0054A7 14               [12]  895 	dec	a
      0054A8 F0               [24]  896 	movx	@dptr,a
                                    897 ;	tmk_core/protocol/ch555/usb_ak820.c:125: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
      0054A9 90 22 00         [24]  898 	mov	dptr,#0x2200
      0054AC 74 CF            [12]  899 	mov	a,#0xcf
      0054AE F0               [24]  900 	movx	@dptr,a
                                    901 ;	tmk_core/protocol/ch555/usb_ak820.c:126: }
      0054AF 22               [24]  902 	ret
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
      0054B0                        913 _control_next:
                                    914 ;	tmk_core/protocol/ch555/usb_ak820.c:130: uint8_t length = D0SetupLen > DEF_ENDP0_SIZE ? DEF_ENDP0_SIZE : D0SetupLen;
      0054B0 90 06 86         [24]  915 	mov	dptr,#_D0SetupLen
      0054B3 E0               [24]  916 	movx	a,@dptr
      0054B4 FE               [12]  917 	mov	r6,a
      0054B5 A3               [24]  918 	inc	dptr
      0054B6 E0               [24]  919 	movx	a,@dptr
      0054B7 FF               [12]  920 	mov	r7,a
      0054B8 C3               [12]  921 	clr	c
      0054B9 74 40            [12]  922 	mov	a,#0x40
      0054BB 9E               [12]  923 	subb	a,r6
      0054BC E4               [12]  924 	clr	a
      0054BD 9F               [12]  925 	subb	a,r7
      0054BE 50 04            [24]  926 	jnc	00109$
                                    927 ;	free result
      0054C0 7E 40            [12]  928 	mov	r6,#0x40
      0054C2 80 07            [24]  929 	sjmp	00110$
      0054C4                        930 00109$:
      0054C4 90 06 86         [24]  931 	mov	dptr,#_D0SetupLen
      0054C7 E0               [24]  932 	movx	a,@dptr
      0054C8 FE               [12]  933 	mov	r6,a
      0054C9 A3               [24]  934 	inc	dptr
      0054CA E0               [24]  935 	movx	a,@dptr
      0054CB                        936 00110$:
                                    937 ;	tmk_core/protocol/ch555/usb_ak820.c:131: for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = *control_pointer++;
      0054CB 7F 00            [12]  938 	mov	r7,#0x00
      0054CD                        939 00105$:
      0054CD C3               [12]  940 	clr	c
      0054CE EF               [12]  941 	mov	a,r7
      0054CF 9E               [12]  942 	subb	a,r6
      0054D0 50 2A            [24]  943 	jnc	00101$
      0054D2 8F 04            [24]  944 	mov	ar4,r7
      0054D4 74 10            [12]  945 	mov	a,#0x10
      0054D6 24 00            [12]  946 	add	a, #0x00
      0054D8 FD               [12]  947 	mov	r5,a
      0054D9 90 06 E8         [24]  948 	mov	dptr,#_control_pointer
      0054DC E0               [24]  949 	movx	a,@dptr
      0054DD FA               [12]  950 	mov	r2,a
      0054DE A3               [24]  951 	inc	dptr
      0054DF E0               [24]  952 	movx	a,@dptr
      0054E0 FB               [12]  953 	mov	r3,a
      0054E1 8A 82            [24]  954 	mov	dpl,r2
      0054E3 8B 83            [24]  955 	mov	dph,r3
      0054E5 E4               [12]  956 	clr	a
      0054E6 93               [24]  957 	movc	a,@a+dptr
      0054E7 F9               [12]  958 	mov	r1,a
      0054E8 90 06 E8         [24]  959 	mov	dptr,#_control_pointer
      0054EB 74 01            [12]  960 	mov	a,#0x01
      0054ED 2A               [12]  961 	add	a, r2
      0054EE F0               [24]  962 	movx	@dptr,a
      0054EF E4               [12]  963 	clr	a
      0054F0 3B               [12]  964 	addc	a, r3
      0054F1 A3               [24]  965 	inc	dptr
      0054F2 F0               [24]  966 	movx	@dptr,a
      0054F3 8C 82            [24]  967 	mov	dpl,r4
      0054F5 8D 83            [24]  968 	mov	dph,r5
      0054F7 E9               [12]  969 	mov	a,r1
      0054F8 F0               [24]  970 	movx	@dptr,a
      0054F9 0F               [12]  971 	inc	r7
      0054FA 80 D1            [24]  972 	sjmp	00105$
      0054FC                        973 00101$:
                                    974 ;	tmk_core/protocol/ch555/usb_ak820.c:132: D0SetupLen -= length;
      0054FC 8E 05            [24]  975 	mov	ar5,r6
      0054FE 7F 00            [12]  976 	mov	r7,#0x00
      005500 90 06 86         [24]  977 	mov	dptr,#_D0SetupLen
      005503 E0               [24]  978 	movx	a,@dptr
      005504 FB               [12]  979 	mov	r3,a
      005505 A3               [24]  980 	inc	dptr
      005506 E0               [24]  981 	movx	a,@dptr
      005507 FC               [12]  982 	mov	r4,a
      005508 EB               [12]  983 	mov	a,r3
      005509 C3               [12]  984 	clr	c
      00550A 9D               [12]  985 	subb	a,r5
      00550B FB               [12]  986 	mov	r3,a
      00550C EC               [12]  987 	mov	a,r4
      00550D 9F               [12]  988 	subb	a,r7
      00550E FC               [12]  989 	mov	r4,a
      00550F 90 06 86         [24]  990 	mov	dptr,#_D0SetupLen
      005512 EB               [12]  991 	mov	a,r3
      005513 F0               [24]  992 	movx	@dptr,a
      005514 EC               [12]  993 	mov	a,r4
      005515 A3               [24]  994 	inc	dptr
      005516 F0               [24]  995 	movx	@dptr,a
                                    996 ;	tmk_core/protocol/ch555/usb_ak820.c:133: if (!length) control_zlp = 0;
      005517 EE               [12]  997 	mov	a,r6
      005518 70 05            [24]  998 	jnz	00103$
      00551A 90 06 E7         [24]  999 	mov	dptr,#_control_zlp
      00551D E4               [12] 1000 	clr	a
      00551E F0               [24] 1001 	movx	@dptr,a
      00551F                       1002 00103$:
                                   1003 ;	tmk_core/protocol/ch555/usb_ak820.c:134: D0_EP0T_L = length;
      00551F 90 22 08         [24] 1004 	mov	dptr,#0x2208
      005522 EE               [12] 1005 	mov	a,r6
      005523 F0               [24] 1006 	movx	@dptr,a
                                   1007 ;	tmk_core/protocol/ch555/usb_ak820.c:135: D0_EP0RES = (D0_EP0RES & (bUEP_T_TOG | bUEP_R_TOG)) | UEP_T_RES_ACK | UEP_R_RES_ACK;
      005524 90 22 00         [24] 1008 	mov	dptr,#0x2200
      005527 E0               [24] 1009 	movx	a,@dptr
      005528 54 C0            [12] 1010 	anl	a,#0xc0
      00552A F0               [24] 1011 	movx	@dptr,a
                                   1012 ;	tmk_core/protocol/ch555/usb_ak820.c:136: }
      00552B 22               [24] 1013 	ret
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
      00552C                       1025 _descriptor_select:
      00552C E5 82            [12] 1026 	mov	a,dpl
      00552E 90 06 ED         [24] 1027 	mov	dptr,#_descriptor_select_type_10000_265
      005531 F0               [24] 1028 	movx	@dptr,a
                                   1029 ;	tmk_core/protocol/ch555/usb_ak820.c:140: if (type == USB_DESCR_TYP_DEVICE && !index && !interface) {
      005532 E0               [24] 1030 	movx	a,@dptr
      005533 FF               [12] 1031 	mov	r7,a
      005534 BF 01 20         [24] 1032 	cjne	r7,#0x01,00102$
      005537 90 06 EA         [24] 1033 	mov	dptr,#_descriptor_select_PARM_2
      00553A E0               [24] 1034 	movx	a,@dptr
      00553B 70 1A            [24] 1035 	jnz	00102$
      00553D 90 06 EB         [24] 1036 	mov	dptr,#_descriptor_select_PARM_3
      005540 E0               [24] 1037 	movx	a,@dptr
      005541 F5 F0            [12] 1038 	mov	b,a
      005543 A3               [24] 1039 	inc	dptr
      005544 E0               [24] 1040 	movx	a,@dptr
      005545 45 F0            [12] 1041 	orl	a,b
      005547 70 0E            [24] 1042 	jnz	00102$
                                   1043 ;	tmk_core/protocol/ch555/usb_ak820.c:141: control_pointer = (const uint8_t __code *)&DeviceDescriptor;
      005549 90 06 E8         [24] 1044 	mov	dptr,#_control_pointer
      00554C 74 8E            [12] 1045 	mov	a,#_DeviceDescriptor
      00554E F0               [24] 1046 	movx	@dptr,a
      00554F 74 BC            [12] 1047 	mov	a,#(_DeviceDescriptor >> 8)
      005551 A3               [24] 1048 	inc	dptr
      005552 F0               [24] 1049 	movx	@dptr,a
                                   1050 ;	tmk_core/protocol/ch555/usb_ak820.c:142: return sizeof(DeviceDescriptor);
      005553 90 00 12         [24] 1051 	mov	dptr,#0x0012
      005556 22               [24] 1052 	ret
      005557                       1053 00102$:
                                   1054 ;	tmk_core/protocol/ch555/usb_ak820.c:144: if (type == USB_DESCR_TYP_CONFIG && !index && !interface) {
      005557 90 06 ED         [24] 1055 	mov	dptr,#_descriptor_select_type_10000_265
      00555A E0               [24] 1056 	movx	a,@dptr
      00555B FF               [12] 1057 	mov	r7,a
      00555C BF 02 20         [24] 1058 	cjne	r7,#0x02,00106$
      00555F 90 06 EA         [24] 1059 	mov	dptr,#_descriptor_select_PARM_2
      005562 E0               [24] 1060 	movx	a,@dptr
      005563 70 1A            [24] 1061 	jnz	00106$
      005565 90 06 EB         [24] 1062 	mov	dptr,#_descriptor_select_PARM_3
      005568 E0               [24] 1063 	movx	a,@dptr
      005569 F5 F0            [12] 1064 	mov	b,a
      00556B A3               [24] 1065 	inc	dptr
      00556C E0               [24] 1066 	movx	a,@dptr
      00556D 45 F0            [12] 1067 	orl	a,b
      00556F 70 0E            [24] 1068 	jnz	00106$
                                   1069 ;	tmk_core/protocol/ch555/usb_ak820.c:145: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor;
      005571 90 06 E8         [24] 1070 	mov	dptr,#_control_pointer
      005574 74 A0            [12] 1071 	mov	a,#_ConfigurationDescriptor
      005576 F0               [24] 1072 	movx	@dptr,a
      005577 74 BC            [12] 1073 	mov	a,#(_ConfigurationDescriptor >> 8)
      005579 A3               [24] 1074 	inc	dptr
      00557A F0               [24] 1075 	movx	@dptr,a
                                   1076 ;	tmk_core/protocol/ch555/usb_ak820.c:146: return sizeof(ConfigurationDescriptor);
      00557B 90 00 54         [24] 1077 	mov	dptr,#0x0054
      00557E 22               [24] 1078 	ret
      00557F                       1079 00106$:
                                   1080 ;	tmk_core/protocol/ch555/usb_ak820.c:148: if (type == USB_DESCR_TYP_STRING) {
      00557F 90 06 ED         [24] 1081 	mov	dptr,#_descriptor_select_type_10000_265
      005582 E0               [24] 1082 	movx	a,@dptr
      005583 FF               [12] 1083 	mov	r7,a
      005584 BF 03 02         [24] 1084 	cjne	r7,#0x03,00278$
      005587 80 03            [24] 1085 	sjmp	00279$
      005589                       1086 00278$:
      005589 02 56 23         [24] 1087 	ljmp	00119$
      00558C                       1088 00279$:
                                   1089 ;	tmk_core/protocol/ch555/usb_ak820.c:149: if (interface != 0 && interface != 0x0409) return 0;
      00558C 90 06 EB         [24] 1090 	mov	dptr,#_descriptor_select_PARM_3
      00558F E0               [24] 1091 	movx	a,@dptr
      005590 FD               [12] 1092 	mov	r5,a
      005591 A3               [24] 1093 	inc	dptr
      005592 E0               [24] 1094 	movx	a,@dptr
      005593 FE               [12] 1095 	mov	r6,a
      005594 90 06 EB         [24] 1096 	mov	dptr,#_descriptor_select_PARM_3
      005597 E0               [24] 1097 	movx	a,@dptr
      005598 F5 F0            [12] 1098 	mov	b,a
      00559A A3               [24] 1099 	inc	dptr
      00559B E0               [24] 1100 	movx	a,@dptr
      00559C 45 F0            [12] 1101 	orl	a,b
      00559E 60 0C            [24] 1102 	jz	00110$
      0055A0 BD 09 05         [24] 1103 	cjne	r5,#0x09,00281$
      0055A3 BE 04 02         [24] 1104 	cjne	r6,#0x04,00281$
      0055A6 80 04            [24] 1105 	sjmp	00110$
      0055A8                       1106 00281$:
      0055A8 90 00 00         [24] 1107 	mov	dptr,#0x0000
      0055AB 22               [24] 1108 	ret
      0055AC                       1109 00110$:
                                   1110 ;	tmk_core/protocol/ch555/usb_ak820.c:150: switch (index) {
      0055AC 90 06 EA         [24] 1111 	mov	dptr,#_descriptor_select_PARM_2
      0055AF E0               [24] 1112 	movx	a,@dptr
      0055B0 FE               [12] 1113 	mov  r6,a
      0055B1 24 FC            [12] 1114 	add	a,#0xff - 0x03
      0055B3 40 6A            [24] 1115 	jc	00116$
                                   1116 ;	free result
      0055B5 EE               [12] 1117 	mov	a,r6
      0055B6 2E               [12] 1118 	add	a,r6
                                   1119 ;	tmk_core/protocol/ch555/usb_ak820.c:151: case 0: control_pointer = (const uint8_t __code *)&LanguageString; return LanguageString.Header.Size;
      0055B7 90 55 BB         [24] 1120 	mov	dptr,#00283$
      0055BA 73               [24] 1121 	jmp	@a+dptr
      0055BB                       1122 00283$:
      0055BB 80 06            [24] 1123 	sjmp	00112$
      0055BD 80 1B            [24] 1124 	sjmp	00113$
      0055BF 80 30            [24] 1125 	sjmp	00114$
      0055C1 80 45            [24] 1126 	sjmp	00115$
      0055C3                       1127 00112$:
      0055C3 90 06 E8         [24] 1128 	mov	dptr,#_control_pointer
      0055C6 74 F4            [12] 1129 	mov	a,#_LanguageString
      0055C8 F0               [24] 1130 	movx	@dptr,a
      0055C9 74 BC            [12] 1131 	mov	a,#(_LanguageString >> 8)
      0055CB A3               [24] 1132 	inc	dptr
      0055CC F0               [24] 1133 	movx	@dptr,a
      0055CD 90 BC F4         [24] 1134 	mov	dptr,#_LanguageString
      0055D0 E4               [12] 1135 	clr	a
      0055D1 93               [24] 1136 	movc	a,@a+dptr
      0055D2 FE               [12] 1137 	mov	r6,a
      0055D3 7D 00            [12] 1138 	mov	r5,#0x00
      0055D5 8E 82            [24] 1139 	mov	dpl, r6
      0055D7 8D 83            [24] 1140 	mov	dph, r5
      0055D9 22               [24] 1141 	ret
                                   1142 ;	tmk_core/protocol/ch555/usb_ak820.c:152: case 1: control_pointer = (const uint8_t __code *)&ManufacturerString; return ManufacturerString.Header.Size;
      0055DA                       1143 00113$:
      0055DA 90 06 E8         [24] 1144 	mov	dptr,#_control_pointer
      0055DD 74 F8            [12] 1145 	mov	a,#_ManufacturerString
      0055DF F0               [24] 1146 	movx	@dptr,a
      0055E0 74 BC            [12] 1147 	mov	a,#(_ManufacturerString >> 8)
      0055E2 A3               [24] 1148 	inc	dptr
      0055E3 F0               [24] 1149 	movx	@dptr,a
      0055E4 90 BC F8         [24] 1150 	mov	dptr,#_ManufacturerString
      0055E7 E4               [12] 1151 	clr	a
      0055E8 93               [24] 1152 	movc	a,@a+dptr
      0055E9 FE               [12] 1153 	mov	r6,a
      0055EA 7D 00            [12] 1154 	mov	r5,#0x00
      0055EC 8E 82            [24] 1155 	mov	dpl, r6
      0055EE 8D 83            [24] 1156 	mov	dph, r5
      0055F0 22               [24] 1157 	ret
                                   1158 ;	tmk_core/protocol/ch555/usb_ak820.c:153: case 2: control_pointer = (const uint8_t __code *)&ProductString; return ProductString.Header.Size;
      0055F1                       1159 00114$:
      0055F1 90 06 E8         [24] 1160 	mov	dptr,#_control_pointer
      0055F4 74 06            [12] 1161 	mov	a,#_ProductString
      0055F6 F0               [24] 1162 	movx	@dptr,a
      0055F7 74 BD            [12] 1163 	mov	a,#(_ProductString >> 8)
      0055F9 A3               [24] 1164 	inc	dptr
      0055FA F0               [24] 1165 	movx	@dptr,a
      0055FB 90 BD 06         [24] 1166 	mov	dptr,#_ProductString
      0055FE E4               [12] 1167 	clr	a
      0055FF 93               [24] 1168 	movc	a,@a+dptr
      005600 FE               [12] 1169 	mov	r6,a
      005601 7D 00            [12] 1170 	mov	r5,#0x00
      005603 8E 82            [24] 1171 	mov	dpl, r6
      005605 8D 83            [24] 1172 	mov	dph, r5
      005607 22               [24] 1173 	ret
                                   1174 ;	tmk_core/protocol/ch555/usb_ak820.c:155: case 3: control_pointer = (const uint8_t __code *)&SerialNumberString; return SerialNumberString.Header.Size;
      005608                       1175 00115$:
      005608 90 06 E8         [24] 1176 	mov	dptr,#_control_pointer
      00560B 74 3E            [12] 1177 	mov	a,#_SerialNumberString
      00560D F0               [24] 1178 	movx	@dptr,a
      00560E 74 BD            [12] 1179 	mov	a,#(_SerialNumberString >> 8)
      005610 A3               [24] 1180 	inc	dptr
      005611 F0               [24] 1181 	movx	@dptr,a
      005612 90 BD 3E         [24] 1182 	mov	dptr,#_SerialNumberString
      005615 E4               [12] 1183 	clr	a
      005616 93               [24] 1184 	movc	a,@a+dptr
      005617 FE               [12] 1185 	mov	r6,a
      005618 7D 00            [12] 1186 	mov	r5,#0x00
      00561A 8E 82            [24] 1187 	mov	dpl, r6
      00561C 8D 83            [24] 1188 	mov	dph, r5
      00561E 22               [24] 1189 	ret
                                   1190 ;	tmk_core/protocol/ch555/usb_ak820.c:157: default: return 0;
      00561F                       1191 00116$:
      00561F 90 00 00         [24] 1192 	mov	dptr,#0x0000
      005622 22               [24] 1193 	ret
                                   1194 ;	tmk_core/protocol/ch555/usb_ak820.c:158: }
      005623                       1195 00119$:
                                   1196 ;	tmk_core/protocol/ch555/usb_ak820.c:160: if (index || interface >= TOTAL_INTERFACES) return 0;
      005623 90 06 EA         [24] 1197 	mov	dptr,#_descriptor_select_PARM_2
      005626 E0               [24] 1198 	movx	a,@dptr
      005627 70 11            [24] 1199 	jnz	00120$
      005629 90 06 EB         [24] 1200 	mov	dptr,#_descriptor_select_PARM_3
      00562C E0               [24] 1201 	movx	a,@dptr
      00562D FD               [12] 1202 	mov	r5,a
      00562E A3               [24] 1203 	inc	dptr
      00562F E0               [24] 1204 	movx	a,@dptr
      005630 FE               [12] 1205 	mov	r6,a
      005631 C3               [12] 1206 	clr	c
      005632 ED               [12] 1207 	mov	a,r5
      005633 94 03            [12] 1208 	subb	a,#0x03
      005635 EE               [12] 1209 	mov	a,r6
      005636 94 00            [12] 1210 	subb	a,#0x00
      005638 40 04            [24] 1211 	jc	00121$
      00563A                       1212 00120$:
      00563A 90 00 00         [24] 1213 	mov	dptr,#0x0000
      00563D 22               [24] 1214 	ret
      00563E                       1215 00121$:
                                   1216 ;	tmk_core/protocol/ch555/usb_ak820.c:161: if (type == USB_DESCR_TYP_REPORT) {
      00563E BF 22 60         [24] 1217 	cjne	r7,#0x22,00128$
                                   1218 ;	tmk_core/protocol/ch555/usb_ak820.c:162: switch (interface) {
      005641 8D 07            [24] 1219 	mov	ar7,r5
      005643 EF               [12] 1220 	mov	a,r7
      005644 60 10            [24] 1221 	jz	00123$
      005646 BD 01 05         [24] 1222 	cjne	r5,#0x01,00289$
      005649 BE 00 02         [24] 1223 	cjne	r6,#0x00,00289$
      00564C 80 21            [24] 1224 	sjmp	00124$
      00564E                       1225 00289$:
                                   1226 ;	tmk_core/protocol/ch555/usb_ak820.c:163: case KEYBOARD_INTERFACE:
      00564E BD 02 50         [24] 1227 	cjne	r5,#0x02,00128$
      005651 BE 00 4D         [24] 1228 	cjne	r6,#0x00,00128$
      005654 80 32            [24] 1229 	sjmp	00125$
      005656                       1230 00123$:
                                   1231 ;	tmk_core/protocol/ch555/usb_ak820.c:164: control_pointer = (const uint8_t __code *)KeyboardReport;
      005656 90 06 E8         [24] 1232 	mov	dptr,#_control_pointer
      005659 74 B2            [12] 1233 	mov	a,#_KeyboardReport
      00565B F0               [24] 1234 	movx	@dptr,a
      00565C 74 BB            [12] 1235 	mov	a,#(_KeyboardReport >> 8)
      00565E A3               [24] 1236 	inc	dptr
      00565F F0               [24] 1237 	movx	@dptr,a
                                   1238 ;	tmk_core/protocol/ch555/usb_ak820.c:165: return ConfigurationDescriptor.Keyboard_HID.HIDReportLength;
      005660 90 BC B9         [24] 1239 	mov	dptr,#(_ConfigurationDescriptor + 0x0019)
      005663 E4               [12] 1240 	clr	a
      005664 93               [24] 1241 	movc	a,@a+dptr
      005665 FC               [12] 1242 	mov	r4,a
      005666 A3               [24] 1243 	inc	dptr
      005667 E4               [12] 1244 	clr	a
      005668 93               [24] 1245 	movc	a,@a+dptr
      005669 FF               [12] 1246 	mov	r7,a
      00566A 8C 82            [24] 1247 	mov	dpl, r4
      00566C 8F 83            [24] 1248 	mov	dph, r7
      00566E 22               [24] 1249 	ret
                                   1250 ;	tmk_core/protocol/ch555/usb_ak820.c:166: case RAW_INTERFACE:
      00566F                       1251 00124$:
                                   1252 ;	tmk_core/protocol/ch555/usb_ak820.c:167: control_pointer = (const uint8_t __code *)RawReport;
      00566F 90 06 E8         [24] 1253 	mov	dptr,#_control_pointer
      005672 74 65            [12] 1254 	mov	a,#_RawReport
      005674 F0               [24] 1255 	movx	@dptr,a
      005675 74 BC            [12] 1256 	mov	a,#(_RawReport >> 8)
      005677 A3               [24] 1257 	inc	dptr
      005678 F0               [24] 1258 	movx	@dptr,a
                                   1259 ;	tmk_core/protocol/ch555/usb_ak820.c:168: return ConfigurationDescriptor.Raw_HID.HIDReportLength;
      005679 90 BC D2         [24] 1260 	mov	dptr,#(_ConfigurationDescriptor + 0x0032)
      00567C E4               [12] 1261 	clr	a
      00567D 93               [24] 1262 	movc	a,@a+dptr
      00567E FC               [12] 1263 	mov	r4,a
      00567F A3               [24] 1264 	inc	dptr
      005680 E4               [12] 1265 	clr	a
      005681 93               [24] 1266 	movc	a,@a+dptr
      005682 FF               [12] 1267 	mov	r7,a
      005683 8C 82            [24] 1268 	mov	dpl, r4
      005685 8F 83            [24] 1269 	mov	dph, r7
      005687 22               [24] 1270 	ret
                                   1271 ;	tmk_core/protocol/ch555/usb_ak820.c:170: case SHARED_INTERFACE:
      005688                       1272 00125$:
                                   1273 ;	tmk_core/protocol/ch555/usb_ak820.c:171: control_pointer = (const uint8_t __code *)SharedReport;
      005688 90 06 E8         [24] 1274 	mov	dptr,#_control_pointer
      00568B 74 F7            [12] 1275 	mov	a,#_SharedReport
      00568D F0               [24] 1276 	movx	@dptr,a
      00568E 74 BB            [12] 1277 	mov	a,#(_SharedReport >> 8)
      005690 A3               [24] 1278 	inc	dptr
      005691 F0               [24] 1279 	movx	@dptr,a
                                   1280 ;	tmk_core/protocol/ch555/usb_ak820.c:172: return ConfigurationDescriptor.Shared_HID.HIDReportLength;
      005692 90 BC EB         [24] 1281 	mov	dptr,#(_ConfigurationDescriptor + 0x004b)
      005695 E4               [12] 1282 	clr	a
      005696 93               [24] 1283 	movc	a,@a+dptr
      005697 FC               [12] 1284 	mov	r4,a
      005698 A3               [24] 1285 	inc	dptr
      005699 E4               [12] 1286 	clr	a
      00569A 93               [24] 1287 	movc	a,@a+dptr
      00569B FF               [12] 1288 	mov	r7,a
      00569C 8C 82            [24] 1289 	mov	dpl, r4
      00569E 8F 83            [24] 1290 	mov	dph, r7
                                   1291 ;	tmk_core/protocol/ch555/usb_ak820.c:174: }
      0056A0 22               [24] 1292 	ret
      0056A1                       1293 00128$:
                                   1294 ;	tmk_core/protocol/ch555/usb_ak820.c:176: if (type == USB_DESCR_TYP_HID) {
      0056A1 90 06 ED         [24] 1295 	mov	dptr,#_descriptor_select_type_10000_265
      0056A4 E0               [24] 1296 	movx	a,@dptr
      0056A5 FF               [12] 1297 	mov	r7,a
      0056A6 BF 21 48         [24] 1298 	cjne	r7,#0x21,00134$
                                   1299 ;	tmk_core/protocol/ch555/usb_ak820.c:177: switch (interface) {
      0056A9 8D 07            [24] 1300 	mov	ar7,r5
      0056AB EF               [12] 1301 	mov	a,r7
      0056AC 60 10            [24] 1302 	jz	00129$
      0056AE BD 01 05         [24] 1303 	cjne	r5,#0x01,00294$
      0056B1 BE 00 02         [24] 1304 	cjne	r6,#0x00,00294$
      0056B4 80 19            [24] 1305 	sjmp	00130$
      0056B6                       1306 00294$:
                                   1307 ;	tmk_core/protocol/ch555/usb_ak820.c:178: case KEYBOARD_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Keyboard_HID; return 9;
      0056B6 BD 02 38         [24] 1308 	cjne	r5,#0x02,00134$
      0056B9 BE 00 35         [24] 1309 	cjne	r6,#0x00,00134$
      0056BC 80 22            [24] 1310 	sjmp	00131$
      0056BE                       1311 00129$:
      0056BE 90 06 E8         [24] 1312 	mov	dptr,#_control_pointer
      0056C1 74 12            [12] 1313 	mov	a,#0x12
      0056C3 24 A0            [12] 1314 	add	a, #_ConfigurationDescriptor
      0056C5 F0               [24] 1315 	movx	@dptr,a
      0056C6 E4               [12] 1316 	clr	a
      0056C7 34 BC            [12] 1317 	addc	a, #(_ConfigurationDescriptor >> 8)
      0056C9 A3               [24] 1318 	inc	dptr
      0056CA F0               [24] 1319 	movx	@dptr,a
      0056CB 90 00 09         [24] 1320 	mov	dptr,#0x0009
                                   1321 ;	tmk_core/protocol/ch555/usb_ak820.c:179: case RAW_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Raw_HID; return 9;
      0056CE 22               [24] 1322 	ret
      0056CF                       1323 00130$:
      0056CF 90 06 E8         [24] 1324 	mov	dptr,#_control_pointer
      0056D2 74 2B            [12] 1325 	mov	a,#0x2b
      0056D4 24 A0            [12] 1326 	add	a, #_ConfigurationDescriptor
      0056D6 F0               [24] 1327 	movx	@dptr,a
      0056D7 E4               [12] 1328 	clr	a
      0056D8 34 BC            [12] 1329 	addc	a, #(_ConfigurationDescriptor >> 8)
      0056DA A3               [24] 1330 	inc	dptr
      0056DB F0               [24] 1331 	movx	@dptr,a
      0056DC 90 00 09         [24] 1332 	mov	dptr,#0x0009
                                   1333 ;	tmk_core/protocol/ch555/usb_ak820.c:181: case SHARED_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Shared_HID; return 9;
      0056DF 22               [24] 1334 	ret
      0056E0                       1335 00131$:
      0056E0 90 06 E8         [24] 1336 	mov	dptr,#_control_pointer
      0056E3 74 44            [12] 1337 	mov	a,#0x44
      0056E5 24 A0            [12] 1338 	add	a, #_ConfigurationDescriptor
      0056E7 F0               [24] 1339 	movx	@dptr,a
      0056E8 E4               [12] 1340 	clr	a
      0056E9 34 BC            [12] 1341 	addc	a, #(_ConfigurationDescriptor >> 8)
      0056EB A3               [24] 1342 	inc	dptr
      0056EC F0               [24] 1343 	movx	@dptr,a
      0056ED 90 00 09         [24] 1344 	mov	dptr,#0x0009
                                   1345 ;	tmk_core/protocol/ch555/usb_ak820.c:183: }
      0056F0 22               [24] 1346 	ret
      0056F1                       1347 00134$:
                                   1348 ;	tmk_core/protocol/ch555/usb_ak820.c:185: return 0;
      0056F1 90 00 00         [24] 1349 	mov	dptr,#0x0000
                                   1350 ;	tmk_core/protocol/ch555/usb_ak820.c:186: }
      0056F4 22               [24] 1351 	ret
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
      0056F5                       1371 _control_setup:
                                   1372 ;	tmk_core/protocol/ch555/usb_ak820.c:189: uint8_t type = pD0_SETUP_REQ->bRequestType;
      0056F5 90 10 00         [24] 1373 	mov	dptr,#0x1000
      0056F8 E0               [24] 1374 	movx	a,@dptr
      0056F9 FF               [12] 1375 	mov	r7,a
                                   1376 ;	tmk_core/protocol/ch555/usb_ak820.c:190: uint16_t value = pD0_SETUP_REQ->wValueL | ((uint16_t)pD0_SETUP_REQ->wValueH << 8);
      0056FA A3               [24] 1377 	inc	dptr
      0056FB A3               [24] 1378 	inc	dptr
      0056FC E0               [24] 1379 	movx	a,@dptr
      0056FD FE               [12] 1380 	mov	r6,a
      0056FE A3               [24] 1381 	inc	dptr
      0056FF E0               [24] 1382 	movx	a,@dptr
      005700 FC               [12] 1383 	mov	r4,a
      005701 7D 00            [12] 1384 	mov	r5,#0x00
      005703 8E 03            [24] 1385 	mov	ar3,r6
      005705 7E 00            [12] 1386 	mov	r6,#0x00
      005707 ED               [12] 1387 	mov	a,r5
      005708 4B               [12] 1388 	orl	a,r3
      005709 FD               [12] 1389 	mov	r5,a
      00570A EC               [12] 1390 	mov	a,r4
      00570B 4E               [12] 1391 	orl	a,r6
      00570C FE               [12] 1392 	mov	r6,a
                                   1393 ;	tmk_core/protocol/ch555/usb_ak820.c:191: uint16_t index = pD0_SETUP_REQ->wIndexL | ((uint16_t)pD0_SETUP_REQ->wIndexH << 8);
      00570D A3               [24] 1394 	inc	dptr
      00570E E0               [24] 1395 	movx	a,@dptr
      00570F FC               [12] 1396 	mov	r4,a
      005710 A3               [24] 1397 	inc	dptr
      005711 E0               [24] 1398 	movx	a,@dptr
      005712 FA               [12] 1399 	mov	r2,a
      005713 7B 00            [12] 1400 	mov	r3,#0x00
      005715 8C 01            [24] 1401 	mov	ar1,r4
      005717 7C 00            [12] 1402 	mov	r4,#0x00
      005719 EB               [12] 1403 	mov	a,r3
      00571A 49               [12] 1404 	orl	a,r1
      00571B FB               [12] 1405 	mov	r3,a
      00571C EA               [12] 1406 	mov	a,r2
      00571D 4C               [12] 1407 	orl	a,r4
      00571E FC               [12] 1408 	mov	r4,a
                                   1409 ;	tmk_core/protocol/ch555/usb_ak820.c:195: uint8_t offset = 0;
      00571F 90 06 F0         [24] 1410 	mov	dptr,#_control_setup_offset_10000_286
      005722 E4               [12] 1411 	clr	a
      005723 F0               [24] 1412 	movx	@dptr,a
                                   1413 ;	tmk_core/protocol/ch555/usb_ak820.c:197: if (raw_state == RAW_RX) raw_state = RAW_IDLE; /* abort only unfinished OUT */
      005724 90 06 93         [24] 1414 	mov	dptr,#_raw_state
      005727 E0               [24] 1415 	movx	a,@dptr
      005728 FA               [12] 1416 	mov	r2,a
      005729 BA 01 05         [24] 1417 	cjne	r2,#0x01,00102$
      00572C 90 06 93         [24] 1418 	mov	dptr,#_raw_state
      00572F E4               [12] 1419 	clr	a
      005730 F0               [24] 1420 	movx	@dptr,a
      005731                       1421 00102$:
                                   1422 ;	tmk_core/protocol/ch555/usb_ak820.c:198: output_kind = OUTPUT_NONE;
      005731 C0 07            [24] 1423 	push	ar7
      005733 90 06 E5         [24] 1424 	mov	dptr,#_output_kind
      005736 E4               [12] 1425 	clr	a
      005737 F0               [24] 1426 	movx	@dptr,a
                                   1427 ;	tmk_core/protocol/ch555/usb_ak820.c:199: control_phase = CTRL_IDLE;
      005738 90 06 E4         [24] 1428 	mov	dptr,#_control_phase
      00573B F0               [24] 1429 	movx	@dptr,a
                                   1430 ;	tmk_core/protocol/ch555/usb_ak820.c:200: control_zlp = 0;
      00573C 90 06 E7         [24] 1431 	mov	dptr,#_control_zlp
      00573F F0               [24] 1432 	movx	@dptr,a
                                   1433 ;	tmk_core/protocol/ch555/usb_ak820.c:201: D0SetupReqCode = pD0_SETUP_REQ->bRequest;
      005740 90 10 01         [24] 1434 	mov	dptr,#0x1001
      005743 E0               [24] 1435 	movx	a,@dptr
      005744 90 06 85         [24] 1436 	mov	dptr,#_D0SetupReqCode
      005747 F0               [24] 1437 	movx	@dptr,a
                                   1438 ;	tmk_core/protocol/ch555/usb_ak820.c:202: D0SetupLen = pD0_SETUP_REQ->wLengthL | ((uint16_t)pD0_SETUP_REQ->wLengthH << 8);
      005748 90 10 06         [24] 1439 	mov	dptr,#0x1006
      00574B E0               [24] 1440 	movx	a,@dptr
      00574C FA               [12] 1441 	mov	r2,a
      00574D A3               [24] 1442 	inc	dptr
      00574E E0               [24] 1443 	movx	a,@dptr
      00574F F9               [12] 1444 	mov	r1,a
      005750 78 00            [12] 1445 	mov	r0,#0x00
      005752 7F 00            [12] 1446 	mov	r7,#0x00
      005754 90 06 86         [24] 1447 	mov	dptr,#_D0SetupLen
      005757 E8               [12] 1448 	mov	a,r0
      005758 4A               [12] 1449 	orl	a,r2
      005759 F0               [24] 1450 	movx	@dptr,a
      00575A E9               [12] 1451 	mov	a,r1
      00575B 4F               [12] 1452 	orl	a,r7
      00575C A3               [24] 1453 	inc	dptr
      00575D F0               [24] 1454 	movx	@dptr,a
                                   1455 ;	tmk_core/protocol/ch555/usb_ak820.c:203: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
      00575E 90 22 00         [24] 1456 	mov	dptr,#0x2200
      005761 74 C2            [12] 1457 	mov	a,#0xc2
      005763 F0               [24] 1458 	movx	@dptr,a
                                   1459 ;	tmk_core/protocol/ch555/usb_ak820.c:204: D0_EP0T_L = 0;
      005764 90 22 08         [24] 1460 	mov	dptr,#0x2208
      005767 E4               [12] 1461 	clr	a
      005768 F0               [24] 1462 	movx	@dptr,a
                                   1463 ;	tmk_core/protocol/ch555/usb_ak820.c:206: if (D0SetupReqCode == USB_GET_DESCRIPTOR && (type == 0x80 || type == 0x81)) {
      005769 90 06 85         [24] 1464 	mov	dptr,#_D0SetupReqCode
      00576C E0               [24] 1465 	movx	a,@dptr
      00576D FF               [12] 1466 	mov	r7,a
      00576E BF 06 02         [24] 1467 	cjne	r7,#0x06,01280$
      005771 80 05            [24] 1468 	sjmp	01281$
      005773                       1469 01280$:
      005773 D0 07            [24] 1470 	pop	ar7
      005775 02 58 31         [24] 1471 	ljmp	00112$
      005778                       1472 01281$:
      005778 D0 07            [24] 1473 	pop	ar7
      00577A BF 80 02         [24] 1474 	cjne	r7,#0x80,01282$
      00577D 80 08            [24] 1475 	sjmp	00111$
      00577F                       1476 01282$:
      00577F BF 81 02         [24] 1477 	cjne	r7,#0x81,01283$
      005782 80 03            [24] 1478 	sjmp	01284$
      005784                       1479 01283$:
      005784 02 58 31         [24] 1480 	ljmp	00112$
      005787                       1481 01284$:
      005787                       1482 00111$:
                                   1483 ;	tmk_core/protocol/ch555/usb_ak820.c:207: if (((value >> 8) == USB_DESCR_TYP_HID || (value >> 8) == USB_DESCR_TYP_REPORT) != (type == 0x81)) {
      005787 8E 01            [24] 1484 	mov	ar1,r6
      005789 B9 21 02         [24] 1485 	cjne	r1,#0x21,01285$
      00578C 80 09            [24] 1486 	sjmp	00301$
      00578E                       1487 01285$:
      00578E B9 22 02         [24] 1488 	cjne	r1,#0x22,01286$
      005791 80 04            [24] 1489 	sjmp	00301$
      005793                       1490 01286$:
                                   1491 ;	assignBit
      005793 C2 09            [12] 1492 	clr	_control_setup_sloc0_1_0
      005795 80 02            [24] 1493 	sjmp	00302$
      005797                       1494 00301$:
                                   1495 ;	assignBit
      005797 D2 09            [12] 1496 	setb	_control_setup_sloc0_1_0
      005799                       1497 00302$:
      005799 E4               [12] 1498 	clr	a
      00579A BF 81 01         [24] 1499 	cjne	r7,#0x81,01287$
      00579D 04               [12] 1500 	inc	a
      00579E                       1501 01287$:
      00579E FA               [12] 1502 	mov	r2,a
      00579F A2 09            [12] 1503 	mov	c,_control_setup_sloc0_1_0
      0057A1 E4               [12] 1504 	clr	a
      0057A2 33               [12] 1505 	rlc	a
      0057A3 B5 02 02         [24] 1506 	cjne	a,ar2,01289$
      0057A6 80 03            [24] 1507 	sjmp	00104$
      0057A8                       1508 01289$:
                                   1509 ;	tmk_core/protocol/ch555/usb_ak820.c:208: control_stall(); return;
      0057A8 02 54 8E         [24] 1510 	ljmp	_control_stall
      0057AB                       1511 00104$:
                                   1512 ;	tmk_core/protocol/ch555/usb_ak820.c:210: length = descriptor_select(value >> 8, value, index);
      0057AB 8E 02            [24] 1513 	mov	ar2,r6
      0057AD 90 06 EA         [24] 1514 	mov	dptr,#_descriptor_select_PARM_2
      0057B0 ED               [12] 1515 	mov	a,r5
      0057B1 F0               [24] 1516 	movx	@dptr,a
      0057B2 90 06 EB         [24] 1517 	mov	dptr,#_descriptor_select_PARM_3
      0057B5 EB               [12] 1518 	mov	a,r3
      0057B6 F0               [24] 1519 	movx	@dptr,a
      0057B7 EC               [12] 1520 	mov	a,r4
      0057B8 A3               [24] 1521 	inc	dptr
      0057B9 F0               [24] 1522 	movx	@dptr,a
      0057BA 8A 82            [24] 1523 	mov	dpl, r2
      0057BC 12 55 2C         [24] 1524 	lcall	_descriptor_select
      0057BF 85 82 24         [24] 1525 	mov	_control_setup_sloc1_1_0,dpl
      0057C2 85 83 25         [24] 1526 	mov	(_control_setup_sloc1_1_0 + 1),dph
                                   1527 ;	tmk_core/protocol/ch555/usb_ak820.c:211: if (!length) { control_stall(); return; }
      0057C5 E5 24            [12] 1528 	mov	a,_control_setup_sloc1_1_0
      0057C7 45 25            [12] 1529 	orl	a,(_control_setup_sloc1_1_0 + 1)
      0057C9 70 03            [24] 1530 	jnz	00106$
      0057CB 02 54 8E         [24] 1531 	ljmp	_control_stall
      0057CE                       1532 00106$:
                                   1533 ;	tmk_core/protocol/ch555/usb_ak820.c:212: control_zlp = length < D0SetupLen && !(length & (DEF_ENDP0_SIZE - 1));
      0057CE 90 06 86         [24] 1534 	mov	dptr,#_D0SetupLen
      0057D1 E0               [24] 1535 	movx	a,@dptr
      0057D2 F8               [12] 1536 	mov	r0,a
      0057D3 A3               [24] 1537 	inc	dptr
      0057D4 E0               [24] 1538 	movx	a,@dptr
      0057D5 FA               [12] 1539 	mov	r2,a
      0057D6 C3               [12] 1540 	clr	c
      0057D7 E5 24            [12] 1541 	mov	a,_control_setup_sloc1_1_0
      0057D9 98               [12] 1542 	subb	a,r0
      0057DA E5 25            [12] 1543 	mov	a,(_control_setup_sloc1_1_0 + 1)
      0057DC 9A               [12] 1544 	subb	a,r2
      0057DD 50 06            [24] 1545 	jnc	00303$
      0057DF E5 24            [12] 1546 	mov	a,_control_setup_sloc1_1_0
      0057E1 54 3F            [12] 1547 	anl	a,#0x3f
      0057E3 60 04            [24] 1548 	jz	00304$
      0057E5                       1549 00303$:
                                   1550 ;	assignBit
      0057E5 C2 09            [12] 1551 	clr	_control_setup_sloc0_1_0
      0057E7 80 02            [24] 1552 	sjmp	00305$
      0057E9                       1553 00304$:
                                   1554 ;	assignBit
      0057E9 D2 09            [12] 1555 	setb	_control_setup_sloc0_1_0
      0057EB                       1556 00305$:
      0057EB 90 06 E7         [24] 1557 	mov	dptr,#_control_zlp
      0057EE A2 09            [12] 1558 	mov	c,_control_setup_sloc0_1_0
      0057F0 E4               [12] 1559 	clr	a
      0057F1 33               [12] 1560 	rlc	a
      0057F2 F0               [24] 1561 	movx	@dptr,a
                                   1562 ;	tmk_core/protocol/ch555/usb_ak820.c:213: if (D0SetupLen > length) D0SetupLen = length;
      0057F3 90 06 86         [24] 1563 	mov	dptr,#_D0SetupLen
      0057F6 E0               [24] 1564 	movx	a,@dptr
      0057F7 F9               [12] 1565 	mov	r1,a
      0057F8 A3               [24] 1566 	inc	dptr
      0057F9 E0               [24] 1567 	movx	a,@dptr
      0057FA FA               [12] 1568 	mov	r2,a
      0057FB C3               [12] 1569 	clr	c
      0057FC E5 24            [12] 1570 	mov	a,_control_setup_sloc1_1_0
      0057FE 99               [12] 1571 	subb	a,r1
      0057FF E5 25            [12] 1572 	mov	a,(_control_setup_sloc1_1_0 + 1)
      005801 9A               [12] 1573 	subb	a,r2
      005802 50 0A            [24] 1574 	jnc	00108$
                                   1575 ;	free result
      005804 90 06 86         [24] 1576 	mov	dptr,#_D0SetupLen
      005807 E5 24            [12] 1577 	mov	a,_control_setup_sloc1_1_0
      005809 F0               [24] 1578 	movx	@dptr,a
      00580A E5 25            [12] 1579 	mov	a,(_control_setup_sloc1_1_0 + 1)
      00580C A3               [24] 1580 	inc	dptr
      00580D F0               [24] 1581 	movx	@dptr,a
      00580E                       1582 00108$:
                                   1583 ;	tmk_core/protocol/ch555/usb_ak820.c:214: control_phase = D0SetupLen ? CTRL_DATA_IN : CTRL_STATUS_OUT;
      00580E 90 06 86         [24] 1584 	mov	dptr,#_D0SetupLen
      005811 E0               [24] 1585 	movx	a,@dptr
      005812 F9               [12] 1586 	mov	r1,a
      005813 A3               [24] 1587 	inc	dptr
      005814 E0               [24] 1588 	movx	a,@dptr
      005815 49               [12] 1589 	orl	a,r1
      005816 60 04            [24] 1590 	jz	00306$
      005818 7A 01            [12] 1591 	mov	r2,#0x01
      00581A 80 02            [24] 1592 	sjmp	00307$
      00581C                       1593 00306$:
      00581C 7A 02            [12] 1594 	mov	r2,#0x02
      00581E                       1595 00307$:
      00581E 90 06 E4         [24] 1596 	mov	dptr,#_control_phase
      005821 EA               [12] 1597 	mov	a,r2
      005822 F0               [24] 1598 	movx	@dptr,a
                                   1599 ;	tmk_core/protocol/ch555/usb_ak820.c:215: if (D0SetupLen) control_next();
      005823 90 06 86         [24] 1600 	mov	dptr,#_D0SetupLen
      005826 E0               [24] 1601 	movx	a,@dptr
      005827 F9               [12] 1602 	mov	r1,a
      005828 A3               [24] 1603 	inc	dptr
      005829 E0               [24] 1604 	movx	a,@dptr
      00582A 49               [12] 1605 	orl	a,r1
      00582B 60 03            [24] 1606 	jz	00110$
                                   1607 ;	tmk_core/protocol/ch555/usb_ak820.c:216: return;
      00582D 02 54 B0         [24] 1608 	ljmp	_control_next
      005830                       1609 00110$:
      005830 22               [24] 1610 	ret
      005831                       1611 00112$:
                                   1612 ;	tmk_core/protocol/ch555/usb_ak820.c:218: if (type == 0x00 && D0SetupReqCode == USB_SET_ADDRESS && !index && !D0SetupLen && value <= 127) {
      005831 EF               [12] 1613 	mov	a,r7
      005832 70 33            [24] 1614 	jnz	00286$
      005834 90 06 85         [24] 1615 	mov	dptr,#_D0SetupReqCode
      005837 E0               [24] 1616 	movx	a,@dptr
      005838 FA               [12] 1617 	mov	r2,a
      005839 BA 05 2B         [24] 1618 	cjne	r2,#0x05,00286$
      00583C EB               [12] 1619 	mov	a,r3
      00583D 4C               [12] 1620 	orl	a,r4
      00583E 70 27            [24] 1621 	jnz	00286$
      005840 90 06 86         [24] 1622 	mov	dptr,#_D0SetupLen
      005843 E0               [24] 1623 	movx	a,@dptr
      005844 F9               [12] 1624 	mov	r1,a
      005845 A3               [24] 1625 	inc	dptr
      005846 E0               [24] 1626 	movx	a,@dptr
      005847 49               [12] 1627 	orl	a,r1
      005848 70 1D            [24] 1628 	jnz	00286$
      00584A 8D 01            [24] 1629 	mov	ar1,r5
      00584C 8E 02            [24] 1630 	mov	ar2,r6
      00584E C3               [12] 1631 	clr	c
      00584F 74 7F            [12] 1632 	mov	a,#0x7f
      005851 99               [12] 1633 	subb	a,r1
      005852 E4               [12] 1634 	clr	a
      005853 9A               [12] 1635 	subb	a,r2
      005854 40 11            [24] 1636 	jc	00286$
                                   1637 ;	free result
                                   1638 ;	tmk_core/protocol/ch555/usb_ak820.c:219: D0SetupLen = value; /* applied after status-IN ACK */
      005856 90 06 86         [24] 1639 	mov	dptr,#_D0SetupLen
      005859 ED               [12] 1640 	mov	a,r5
      00585A F0               [24] 1641 	movx	@dptr,a
      00585B EE               [12] 1642 	mov	a,r6
      00585C A3               [24] 1643 	inc	dptr
      00585D F0               [24] 1644 	movx	@dptr,a
                                   1645 ;	tmk_core/protocol/ch555/usb_ak820.c:220: control_phase = CTRL_STATUS_IN;
      00585E 90 06 E4         [24] 1646 	mov	dptr,#_control_phase
      005861 74 03            [12] 1647 	mov	a,#0x03
      005863 F0               [24] 1648 	movx	@dptr,a
      005864 02 5E F9         [24] 1649 	ljmp	00287$
      005867                       1650 00286$:
                                   1651 ;	tmk_core/protocol/ch555/usb_ak820.c:221: } else if (type == 0x00 && D0SetupReqCode == USB_SET_CONFIGURATION && !index && !D0SetupLen && value <= 1) {
      005867 EF               [12] 1652 	mov	a,r7
      005868 70 4F            [24] 1653 	jnz	00279$
      00586A 90 06 85         [24] 1654 	mov	dptr,#_D0SetupReqCode
      00586D E0               [24] 1655 	movx	a,@dptr
      00586E FA               [12] 1656 	mov	r2,a
      00586F BA 09 47         [24] 1657 	cjne	r2,#0x09,00279$
      005872 EB               [12] 1658 	mov	a,r3
      005873 4C               [12] 1659 	orl	a,r4
      005874 70 43            [24] 1660 	jnz	00279$
      005876 90 06 86         [24] 1661 	mov	dptr,#_D0SetupLen
      005879 E0               [24] 1662 	movx	a,@dptr
      00587A F9               [12] 1663 	mov	r1,a
      00587B A3               [24] 1664 	inc	dptr
      00587C E0               [24] 1665 	movx	a,@dptr
      00587D 49               [12] 1666 	orl	a,r1
      00587E 70 39            [24] 1667 	jnz	00279$
      005880 8D 01            [24] 1668 	mov	ar1,r5
      005882 8E 02            [24] 1669 	mov	ar2,r6
      005884 C3               [12] 1670 	clr	c
      005885 74 01            [12] 1671 	mov	a,#0x01
      005887 99               [12] 1672 	subb	a,r1
      005888 E4               [12] 1673 	clr	a
      005889 9A               [12] 1674 	subb	a,r2
      00588A 40 2D            [24] 1675 	jc	00279$
                                   1676 ;	free result
                                   1677 ;	tmk_core/protocol/ch555/usb_ak820.c:222: endpoints_reset();
      00588C C0 06            [24] 1678 	push	ar6
      00588E C0 05            [24] 1679 	push	ar5
      005890 12 54 37         [24] 1680 	lcall	_endpoints_reset
      005893 D0 05            [24] 1681 	pop	ar5
      005895 D0 06            [24] 1682 	pop	ar6
                                   1683 ;	tmk_core/protocol/ch555/usb_ak820.c:223: D0UsbConfig = value;
      005897 90 06 8B         [24] 1684 	mov	dptr,#_D0UsbConfig
      00589A ED               [12] 1685 	mov	a,r5
      00589B F0               [24] 1686 	movx	@dptr,a
                                   1687 ;	tmk_core/protocol/ch555/usb_ak820.c:224: USB_EnumStatus = value != 0;
      00589C ED               [12] 1688 	mov	a,r5
      00589D 4E               [12] 1689 	orl	a,r6
      00589E B4 01 00         [24] 1690 	cjne	a,#0x01,01308$
      0058A1                       1691 01308$:
      0058A1 B3               [12] 1692 	cpl	c
      0058A2 92 09            [24] 1693 	mov	_control_setup_sloc0_1_0,c
      0058A4 90 06 8C         [24] 1694 	mov	dptr,#_USB_EnumStatus
      0058A7 E4               [12] 1695 	clr	a
      0058A8 33               [12] 1696 	rlc	a
      0058A9 F0               [24] 1697 	movx	@dptr,a
                                   1698 ;	tmk_core/protocol/ch555/usb_ak820.c:225: keyboard_reset = 1;
      0058AA 90 06 B5         [24] 1699 	mov	dptr,#_keyboard_reset
      0058AD 74 01            [12] 1700 	mov	a,#0x01
      0058AF F0               [24] 1701 	movx	@dptr,a
                                   1702 ;	tmk_core/protocol/ch555/usb_ak820.c:226: control_phase = CTRL_STATUS_IN;
      0058B0 90 06 E4         [24] 1703 	mov	dptr,#_control_phase
      0058B3 74 03            [12] 1704 	mov	a,#0x03
      0058B5 F0               [24] 1705 	movx	@dptr,a
      0058B6 02 5E F9         [24] 1706 	ljmp	00287$
      0058B9                       1707 00279$:
                                   1708 ;	tmk_core/protocol/ch555/usb_ak820.c:227: } else if (type == 0x80 && D0SetupReqCode == USB_GET_CONFIGURATION && !index && !value && D0SetupLen == 1) {
      0058B9 E4               [12] 1709 	clr	a
      0058BA BF 80 01         [24] 1710 	cjne	r7,#0x80,01309$
      0058BD 04               [12] 1711 	inc	a
      0058BE                       1712 01309$:
      0058BE FA               [12] 1713 	mov	r2,a
      0058BF 60 34            [24] 1714 	jz	00272$
      0058C1 90 06 85         [24] 1715 	mov	dptr,#_D0SetupReqCode
      0058C4 E0               [24] 1716 	movx	a,@dptr
      0058C5 F9               [12] 1717 	mov	r1,a
      0058C6 B9 08 2C         [24] 1718 	cjne	r1,#0x08,00272$
      0058C9 EB               [12] 1719 	mov	a,r3
      0058CA 4C               [12] 1720 	orl	a,r4
      0058CB 70 28            [24] 1721 	jnz	00272$
      0058CD ED               [12] 1722 	mov	a,r5
      0058CE 4E               [12] 1723 	orl	a,r6
      0058CF 70 24            [24] 1724 	jnz	00272$
      0058D1 90 06 86         [24] 1725 	mov	dptr,#_D0SetupLen
      0058D4 E0               [24] 1726 	movx	a,@dptr
      0058D5 F8               [12] 1727 	mov	r0,a
      0058D6 A3               [24] 1728 	inc	dptr
      0058D7 E0               [24] 1729 	movx	a,@dptr
      0058D8 F9               [12] 1730 	mov	r1,a
      0058D9 B8 01 19         [24] 1731 	cjne	r0,#0x01,00272$
      0058DC B9 00 16         [24] 1732 	cjne	r1,#0x00,00272$
                                   1733 ;	tmk_core/protocol/ch555/usb_ak820.c:228: pD0_EP0_BUF[0] = D0UsbConfig;
      0058DF 90 06 8B         [24] 1734 	mov	dptr,#_D0UsbConfig
      0058E2 E0               [24] 1735 	movx	a,@dptr
      0058E3 90 10 00         [24] 1736 	mov	dptr,#0x1000
      0058E6 F0               [24] 1737 	movx	@dptr,a
                                   1738 ;	tmk_core/protocol/ch555/usb_ak820.c:229: D0_EP0T_L = 1;
      0058E7 90 22 08         [24] 1739 	mov	dptr,#0x2208
      0058EA 74 01            [12] 1740 	mov	a,#0x01
      0058EC F0               [24] 1741 	movx	@dptr,a
                                   1742 ;	tmk_core/protocol/ch555/usb_ak820.c:230: control_phase = CTRL_STATUS_OUT;
      0058ED 90 06 E4         [24] 1743 	mov	dptr,#_control_phase
      0058F0 04               [12] 1744 	inc	a
      0058F1 F0               [24] 1745 	movx	@dptr,a
      0058F2 02 5E F9         [24] 1746 	ljmp	00287$
      0058F5                       1747 00272$:
                                   1748 ;	tmk_core/protocol/ch555/usb_ak820.c:231: } else if (type == 0x81 && D0SetupReqCode == USB_GET_INTERFACE && index < TOTAL_INTERFACES && !value && D0SetupLen == 1 && D0UsbConfig) {
      0058F5 E4               [12] 1749 	clr	a
      0058F6 BF 81 01         [24] 1750 	cjne	r7,#0x81,01318$
      0058F9 04               [12] 1751 	inc	a
      0058FA                       1752 01318$:
      0058FA F5 24            [12] 1753 	mov	_control_setup_sloc1_1_0,a
      0058FC 60 3B            [24] 1754 	jz	00264$
      0058FE 90 06 85         [24] 1755 	mov	dptr,#_D0SetupReqCode
      005901 E0               [24] 1756 	movx	a,@dptr
      005902 F8               [12] 1757 	mov	r0,a
      005903 B8 0A 33         [24] 1758 	cjne	r0,#0x0a,00264$
      005906 C3               [12] 1759 	clr	c
      005907 EB               [12] 1760 	mov	a,r3
      005908 94 03            [12] 1761 	subb	a,#0x03
      00590A EC               [12] 1762 	mov	a,r4
      00590B 94 00            [12] 1763 	subb	a,#0x00
      00590D 50 2A            [24] 1764 	jnc	00264$
      00590F ED               [12] 1765 	mov	a,r5
      005910 4E               [12] 1766 	orl	a,r6
      005911 70 26            [24] 1767 	jnz	00264$
      005913 90 06 86         [24] 1768 	mov	dptr,#_D0SetupLen
      005916 E0               [24] 1769 	movx	a,@dptr
      005917 F8               [12] 1770 	mov	r0,a
      005918 A3               [24] 1771 	inc	dptr
      005919 E0               [24] 1772 	movx	a,@dptr
      00591A F9               [12] 1773 	mov	r1,a
      00591B B8 01 1B         [24] 1774 	cjne	r0,#0x01,00264$
      00591E B9 00 18         [24] 1775 	cjne	r1,#0x00,00264$
      005921 90 06 8B         [24] 1776 	mov	dptr,#_D0UsbConfig
      005924 E0               [24] 1777 	movx	a,@dptr
      005925 60 12            [24] 1778 	jz	00264$
                                   1779 ;	tmk_core/protocol/ch555/usb_ak820.c:232: pD0_EP0_BUF[0] = 0;
      005927 90 10 00         [24] 1780 	mov	dptr,#0x1000
      00592A E4               [12] 1781 	clr	a
      00592B F0               [24] 1782 	movx	@dptr,a
                                   1783 ;	tmk_core/protocol/ch555/usb_ak820.c:233: D0_EP0T_L = 1;
      00592C 90 22 08         [24] 1784 	mov	dptr,#0x2208
      00592F 04               [12] 1785 	inc	a
      005930 F0               [24] 1786 	movx	@dptr,a
                                   1787 ;	tmk_core/protocol/ch555/usb_ak820.c:234: control_phase = CTRL_STATUS_OUT;
      005931 90 06 E4         [24] 1788 	mov	dptr,#_control_phase
      005934 04               [12] 1789 	inc	a
      005935 F0               [24] 1790 	movx	@dptr,a
      005936 02 5E F9         [24] 1791 	ljmp	00287$
      005939                       1792 00264$:
                                   1793 ;	tmk_core/protocol/ch555/usb_ak820.c:235: } else if (type == 0x01 && D0SetupReqCode == USB_SET_INTERFACE && index < TOTAL_INTERFACES && !value && !D0SetupLen && D0UsbConfig) {
      005939 BF 01 2E         [24] 1794 	cjne	r7,#0x01,00256$
      00593C 90 06 85         [24] 1795 	mov	dptr,#_D0SetupReqCode
      00593F E0               [24] 1796 	movx	a,@dptr
      005940 F8               [12] 1797 	mov	r0,a
      005941 B8 0B 26         [24] 1798 	cjne	r0,#0x0b,00256$
      005944 C3               [12] 1799 	clr	c
      005945 EB               [12] 1800 	mov	a,r3
      005946 94 03            [12] 1801 	subb	a,#0x03
      005948 EC               [12] 1802 	mov	a,r4
      005949 94 00            [12] 1803 	subb	a,#0x00
      00594B 50 1D            [24] 1804 	jnc	00256$
      00594D ED               [12] 1805 	mov	a,r5
      00594E 4E               [12] 1806 	orl	a,r6
      00594F 70 19            [24] 1807 	jnz	00256$
      005951 90 06 86         [24] 1808 	mov	dptr,#_D0SetupLen
      005954 E0               [24] 1809 	movx	a,@dptr
      005955 F8               [12] 1810 	mov	r0,a
      005956 A3               [24] 1811 	inc	dptr
      005957 E0               [24] 1812 	movx	a,@dptr
      005958 48               [12] 1813 	orl	a,r0
      005959 70 0F            [24] 1814 	jnz	00256$
      00595B 90 06 8B         [24] 1815 	mov	dptr,#_D0UsbConfig
      00595E E0               [24] 1816 	movx	a,@dptr
      00595F 60 09            [24] 1817 	jz	00256$
                                   1818 ;	tmk_core/protocol/ch555/usb_ak820.c:236: control_phase = CTRL_STATUS_IN;
      005961 90 06 E4         [24] 1819 	mov	dptr,#_control_phase
      005964 74 03            [12] 1820 	mov	a,#0x03
      005966 F0               [24] 1821 	movx	@dptr,a
      005967 02 5E F9         [24] 1822 	ljmp	00287$
      00596A                       1823 00256$:
                                   1824 ;	tmk_core/protocol/ch555/usb_ak820.c:237: } else if (D0SetupReqCode == USB_GET_STATUS && !value && D0SetupLen == 2 &&
      00596A 90 06 85         [24] 1825 	mov	dptr,#_D0SetupReqCode
      00596D E0               [24] 1826 	movx	a,@dptr
      00596E 60 03            [24] 1827 	jz	01336$
      005970 02 5A 1A         [24] 1828 	ljmp	00240$
      005973                       1829 01336$:
      005973 ED               [12] 1830 	mov	a,r5
      005974 4E               [12] 1831 	orl	a,r6
      005975 60 03            [24] 1832 	jz	01337$
      005977 02 5A 1A         [24] 1833 	ljmp	00240$
      00597A                       1834 01337$:
      00597A 90 06 86         [24] 1835 	mov	dptr,#_D0SetupLen
      00597D E0               [24] 1836 	movx	a,@dptr
      00597E F8               [12] 1837 	mov	r0,a
      00597F A3               [24] 1838 	inc	dptr
      005980 E0               [24] 1839 	movx	a,@dptr
      005981 F9               [12] 1840 	mov	r1,a
      005982 B8 02 05         [24] 1841 	cjne	r0,#0x02,01338$
      005985 B9 00 02         [24] 1842 	cjne	r1,#0x00,01338$
      005988 80 03            [24] 1843 	sjmp	01339$
      00598A                       1844 01338$:
      00598A 02 5A 1A         [24] 1845 	ljmp	00240$
      00598D                       1846 01339$:
                                   1847 ;	tmk_core/protocol/ch555/usb_ak820.c:238: ((type == 0x80 && !index) || (type == 0x81 && index < TOTAL_INTERFACES && D0UsbConfig) ||
      00598D EA               [12] 1848 	mov	a,r2
      00598E 60 04            [24] 1849 	jz	00247$
      005990 EB               [12] 1850 	mov	a,r3
      005991 4C               [12] 1851 	orl	a,r4
      005992 60 3C            [24] 1852 	jz	00239$
      005994                       1853 00247$:
      005994 E5 24            [12] 1854 	mov	a,_control_setup_sloc1_1_0
      005996 60 0F            [24] 1855 	jz	00253$
      005998 C3               [12] 1856 	clr	c
      005999 EB               [12] 1857 	mov	a,r3
      00599A 94 03            [12] 1858 	subb	a,#0x03
      00599C EC               [12] 1859 	mov	a,r4
      00599D 94 00            [12] 1860 	subb	a,#0x00
      00599F 50 06            [24] 1861 	jnc	00253$
      0059A1 90 06 8B         [24] 1862 	mov	dptr,#_D0UsbConfig
      0059A4 E0               [24] 1863 	movx	a,@dptr
      0059A5 70 29            [24] 1864 	jnz	00239$
      0059A7                       1865 00253$:
                                   1866 ;	tmk_core/protocol/ch555/usb_ak820.c:239: (type == 0x82 && D0UsbConfig && (index == 0 || index == 0x80 || (index >= 0x81 && index <= 0x83))))) {
      0059A7 BF 82 70         [24] 1867 	cjne	r7,#0x82,00240$
      0059AA 90 06 8B         [24] 1868 	mov	dptr,#_D0UsbConfig
      0059AD E0               [24] 1869 	movx	a,@dptr
      0059AE 60 6A            [24] 1870 	jz	00240$
      0059B0 EB               [12] 1871 	mov	a,r3
      0059B1 4C               [12] 1872 	orl	a,r4
      0059B2 60 1C            [24] 1873 	jz	00239$
      0059B4 8B 00            [24] 1874 	mov	ar0,r3
      0059B6 8C 01            [24] 1875 	mov	ar1,r4
      0059B8 B8 80 05         [24] 1876 	cjne	r0,#0x80,01349$
      0059BB B9 00 02         [24] 1877 	cjne	r1,#0x00,01349$
      0059BE 80 10            [24] 1878 	sjmp	00239$
      0059C0                       1879 01349$:
      0059C0 C3               [12] 1880 	clr	c
      0059C1 E8               [12] 1881 	mov	a,r0
      0059C2 94 81            [12] 1882 	subb	a,#0x81
      0059C4 E9               [12] 1883 	mov	a,r1
      0059C5 94 00            [12] 1884 	subb	a,#0x00
      0059C7 40 51            [24] 1885 	jc	00240$
      0059C9 74 83            [12] 1886 	mov	a,#0x83
      0059CB 98               [12] 1887 	subb	a,r0
      0059CC E4               [12] 1888 	clr	a
      0059CD 99               [12] 1889 	subb	a,r1
      0059CE 40 4A            [24] 1890 	jc	00240$
                                   1891 ;	free result
      0059D0                       1892 00239$:
                                   1893 ;	tmk_core/protocol/ch555/usb_ak820.c:240: endpoint = index & 7;
      0059D0 8B 01            [24] 1894 	mov	ar1,r3
      0059D2 53 01 07         [24] 1895 	anl	ar1,#0x07
                                   1896 ;	tmk_core/protocol/ch555/usb_ak820.c:241: pD0_EP0_BUF[0] = type == 0x80 ? ((USB_SleepStatus & 1) << 1) :
      0059D5 EA               [12] 1897 	mov	a,r2
      0059D6 60 0B            [24] 1898 	jz	00308$
      0059D8 90 06 8D         [24] 1899 	mov	dptr,#_USB_SleepStatus
      0059DB E0               [24] 1900 	movx	a,@dptr
      0059DC 54 01            [12] 1901 	anl	a,#0x01
      0059DE 25 E0            [12] 1902 	add	a,acc
      0059E0 FA               [12] 1903 	mov	r2,a
      0059E1 80 22            [24] 1904 	sjmp	00309$
      0059E3                       1905 00308$:
                                   1906 ;	tmk_core/protocol/ch555/usb_ak820.c:242: ((type == 0x82 && endpoint && (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_STALL) ? 1 : 0);
      0059E3 BF 82 1B         [24] 1907 	cjne	r7,#0x82,00310$
      0059E6 E9               [12] 1908 	mov	a,r1
      0059E7 60 18            [24] 1909 	jz	00310$
      0059E9 89 00            [24] 1910 	mov	ar0,r1
      0059EB 79 00            [12] 1911 	mov	r1,#0x00
      0059ED 74 22            [12] 1912 	mov	a,#0x22
      0059EF 29               [12] 1913 	add	a, r1
      0059F0 F9               [12] 1914 	mov	r1,a
      0059F1 88 82            [24] 1915 	mov	dpl,r0
      0059F3 89 83            [24] 1916 	mov	dph,r1
      0059F5 E0               [24] 1917 	movx	a,@dptr
      0059F6 F9               [12] 1918 	mov	r1,a
      0059F7 53 01 03         [24] 1919 	anl	ar1,#0x03
      0059FA B9 03 04         [24] 1920 	cjne	r1,#0x03,00310$
      0059FD 79 01            [12] 1921 	mov	r1,#0x01
      0059FF 80 02            [24] 1922 	sjmp	00311$
      005A01                       1923 00310$:
      005A01 79 00            [12] 1924 	mov	r1,#0x00
      005A03                       1925 00311$:
      005A03 89 02            [24] 1926 	mov	ar2,r1
      005A05                       1927 00309$:
      005A05 90 10 00         [24] 1928 	mov	dptr,#0x1000
      005A08 EA               [12] 1929 	mov	a,r2
      005A09 F0               [24] 1930 	movx	@dptr,a
                                   1931 ;	tmk_core/protocol/ch555/usb_ak820.c:243: pD0_EP0_BUF[1] = 0;
      005A0A A3               [24] 1932 	inc	dptr
      005A0B E4               [12] 1933 	clr	a
      005A0C F0               [24] 1934 	movx	@dptr,a
                                   1935 ;	tmk_core/protocol/ch555/usb_ak820.c:244: D0_EP0T_L = 2;
      005A0D 90 22 08         [24] 1936 	mov	dptr,#0x2208
      005A10 74 02            [12] 1937 	mov	a,#0x02
      005A12 F0               [24] 1938 	movx	@dptr,a
                                   1939 ;	tmk_core/protocol/ch555/usb_ak820.c:245: control_phase = CTRL_STATUS_OUT;
      005A13 90 06 E4         [24] 1940 	mov	dptr,#_control_phase
      005A16 F0               [24] 1941 	movx	@dptr,a
      005A17 02 5E F9         [24] 1942 	ljmp	00287$
      005A1A                       1943 00240$:
                                   1944 ;	tmk_core/protocol/ch555/usb_ak820.c:246: } else if ((D0SetupReqCode == USB_SET_FEATURE || D0SetupReqCode == USB_CLEAR_FEATURE) && !D0SetupLen && D0UsbConfig) {
      005A1A 90 06 85         [24] 1945 	mov	dptr,#_D0SetupReqCode
      005A1D E0               [24] 1946 	movx	a,@dptr
      005A1E FA               [12] 1947 	mov	r2,a
      005A1F BA 03 02         [24] 1948 	cjne	r2,#0x03,01358$
      005A22 80 0D            [24] 1949 	sjmp	00237$
      005A24                       1950 01358$:
      005A24 90 06 85         [24] 1951 	mov	dptr,#_D0SetupReqCode
      005A27 E0               [24] 1952 	movx	a,@dptr
      005A28 FA               [12] 1953 	mov	r2,a
      005A29 BA 01 02         [24] 1954 	cjne	r2,#0x01,01359$
      005A2C 80 03            [24] 1955 	sjmp	01360$
      005A2E                       1956 01359$:
      005A2E 02 5A CD         [24] 1957 	ljmp	00234$
      005A31                       1958 01360$:
      005A31                       1959 00237$:
      005A31 90 06 86         [24] 1960 	mov	dptr,#_D0SetupLen
      005A34 E0               [24] 1961 	movx	a,@dptr
      005A35 F9               [12] 1962 	mov	r1,a
      005A36 A3               [24] 1963 	inc	dptr
      005A37 E0               [24] 1964 	movx	a,@dptr
      005A38 49               [12] 1965 	orl	a,r1
      005A39 60 03            [24] 1966 	jz	01361$
      005A3B 02 5A CD         [24] 1967 	ljmp	00234$
      005A3E                       1968 01361$:
      005A3E 90 06 8B         [24] 1969 	mov	dptr,#_D0UsbConfig
      005A41 E0               [24] 1970 	movx	a,@dptr
      005A42 70 03            [24] 1971 	jnz	01362$
      005A44 02 5A CD         [24] 1972 	ljmp	00234$
      005A47                       1973 01362$:
                                   1974 ;	tmk_core/protocol/ch555/usb_ak820.c:247: if (type == 0x00 && value == 1 && !index) {
      005A47 EF               [12] 1975 	mov	a,r7
      005A48 70 2A            [24] 1976 	jnz	00127$
      005A4A 8D 01            [24] 1977 	mov	ar1,r5
      005A4C 8E 02            [24] 1978 	mov	ar2,r6
      005A4E B9 01 23         [24] 1979 	cjne	r1,#0x01,00127$
      005A51 BA 00 20         [24] 1980 	cjne	r2,#0x00,00127$
      005A54 EB               [12] 1981 	mov	a,r3
      005A55 4C               [12] 1982 	orl	a,r4
      005A56 70 1C            [24] 1983 	jnz	00127$
                                   1984 ;	tmk_core/protocol/ch555/usb_ak820.c:248: if (D0SetupReqCode == USB_SET_FEATURE) USB_SleepStatus |= 1;
      005A58 90 06 85         [24] 1985 	mov	dptr,#_D0SetupReqCode
      005A5B E0               [24] 1986 	movx	a,@dptr
      005A5C FA               [12] 1987 	mov	r2,a
      005A5D BA 03 0A         [24] 1988 	cjne	r2,#0x03,00116$
      005A60 90 06 8D         [24] 1989 	mov	dptr,#_USB_SleepStatus
      005A63 E0               [24] 1990 	movx	a,@dptr
      005A64 43 E0 01         [24] 1991 	orl	acc,#0x01
      005A67 F0               [24] 1992 	movx	@dptr,a
      005A68 80 5A            [24] 1993 	sjmp	00128$
      005A6A                       1994 00116$:
                                   1995 ;	tmk_core/protocol/ch555/usb_ak820.c:249: else USB_SleepStatus &= ~1;
      005A6A 90 06 8D         [24] 1996 	mov	dptr,#_USB_SleepStatus
      005A6D E0               [24] 1997 	movx	a,@dptr
      005A6E 53 E0 FE         [24] 1998 	anl	acc,#0xfe
      005A71 F0               [24] 1999 	movx	@dptr,a
      005A72 80 50            [24] 2000 	sjmp	00128$
      005A74                       2001 00127$:
                                   2002 ;	tmk_core/protocol/ch555/usb_ak820.c:250: } else if (type == 0x02 && !value && index >= 0x81 && index <= 0x83) {
      005A74 BF 02 4A         [24] 2003 	cjne	r7,#0x02,00121$
      005A77 ED               [12] 2004 	mov	a,r5
      005A78 4E               [12] 2005 	orl	a,r6
      005A79 70 46            [24] 2006 	jnz	00121$
      005A7B 8B 01            [24] 2007 	mov	ar1,r3
      005A7D 8C 02            [24] 2008 	mov	ar2,r4
      005A7F C3               [12] 2009 	clr	c
      005A80 E9               [12] 2010 	mov	a,r1
      005A81 94 81            [12] 2011 	subb	a,#0x81
      005A83 EA               [12] 2012 	mov	a,r2
      005A84 94 00            [12] 2013 	subb	a,#0x00
      005A86 40 39            [24] 2014 	jc	00121$
      005A88 74 83            [12] 2015 	mov	a,#0x83
      005A8A 99               [12] 2016 	subb	a,r1
      005A8B E4               [12] 2017 	clr	a
      005A8C 9A               [12] 2018 	subb	a,r2
      005A8D 40 32            [24] 2019 	jc	00121$
                                   2020 ;	free result
                                   2021 ;	tmk_core/protocol/ch555/usb_ak820.c:251: endpoint = index & 7;
      005A8F 8B 02            [24] 2022 	mov	ar2,r3
      005A91 53 02 07         [24] 2023 	anl	ar2,#0x07
                                   2024 ;	tmk_core/protocol/ch555/usb_ak820.c:253: EP_RESPONSE(endpoint) = bUEP_X_AUTO_TOG | (D0SetupReqCode == USB_SET_FEATURE ? UEP_X_RES_STALL : UEP_X_RES_NAK);
      005A94 8A 00            [24] 2025 	mov	ar0,r2
      005A96 79 00            [12] 2026 	mov	r1,#0x00
      005A98 74 22            [12] 2027 	mov	a,#0x22
      005A9A 29               [12] 2028 	add	a, r1
      005A9B F9               [12] 2029 	mov	r1,a
      005A9C 88 24            [24] 2030 	mov	_control_setup_sloc1_1_0,r0
      005A9E 89 25            [24] 2031 	mov	(_control_setup_sloc1_1_0 + 1),r1
      005AA0 90 06 85         [24] 2032 	mov	dptr,#_D0SetupReqCode
      005AA3 E0               [24] 2033 	movx	a,@dptr
      005AA4 F9               [12] 2034 	mov	r1,a
      005AA5 B9 03 04         [24] 2035 	cjne	r1,#0x03,00318$
      005AA8 79 03            [12] 2036 	mov	r1,#0x03
      005AAA 80 02            [24] 2037 	sjmp	00319$
      005AAC                       2038 00318$:
      005AAC 79 02            [12] 2039 	mov	r1,#0x02
      005AAE                       2040 00319$:
      005AAE 43 01 10         [24] 2041 	orl	ar1,#0x10
      005AB1 85 24 82         [24] 2042 	mov	dpl,_control_setup_sloc1_1_0
      005AB4 85 25 83         [24] 2043 	mov	dph,(_control_setup_sloc1_1_0 + 1)
      005AB7 E9               [12] 2044 	mov	a,r1
      005AB8 F0               [24] 2045 	movx	@dptr,a
                                   2046 ;	tmk_core/protocol/ch555/usb_ak820.c:254: if (endpoint == RAW_IN_EPNUM) raw_complete();
      005AB9 BA 03 08         [24] 2047 	cjne	r2,#0x03,00128$
      005ABC 12 54 1A         [24] 2048 	lcall	_raw_complete
      005ABF 80 03            [24] 2049 	sjmp	00128$
      005AC1                       2050 00121$:
                                   2051 ;	tmk_core/protocol/ch555/usb_ak820.c:255: } else { control_stall(); return; }
      005AC1 02 54 8E         [24] 2052 	ljmp	_control_stall
      005AC4                       2053 00128$:
                                   2054 ;	tmk_core/protocol/ch555/usb_ak820.c:256: control_phase = CTRL_STATUS_IN;
      005AC4 90 06 E4         [24] 2055 	mov	dptr,#_control_phase
      005AC7 74 03            [12] 2056 	mov	a,#0x03
      005AC9 F0               [24] 2057 	movx	@dptr,a
      005ACA 02 5E F9         [24] 2058 	ljmp	00287$
      005ACD                       2059 00234$:
                                   2060 ;	tmk_core/protocol/ch555/usb_ak820.c:257: } else if (type == 0xa1 && D0SetupReqCode == HID_GET_REPORT && D0UsbConfig && D0SetupLen) {
      005ACD E4               [12] 2061 	clr	a
      005ACE BF A1 01         [24] 2062 	cjne	r7,#0xa1,01378$
      005AD1 04               [12] 2063 	inc	a
      005AD2                       2064 01378$:
      005AD2 FA               [12] 2065 	mov	r2,a
      005AD3 70 03            [24] 2066 	jnz	01380$
      005AD5 02 5D 4F         [24] 2067 	ljmp	00228$
      005AD8                       2068 01380$:
      005AD8 90 06 85         [24] 2069 	mov	dptr,#_D0SetupReqCode
      005ADB E0               [24] 2070 	movx	a,@dptr
      005ADC F9               [12] 2071 	mov	r1,a
      005ADD B9 01 02         [24] 2072 	cjne	r1,#0x01,01381$
      005AE0 80 03            [24] 2073 	sjmp	01382$
      005AE2                       2074 01381$:
      005AE2 02 5D 4F         [24] 2075 	ljmp	00228$
      005AE5                       2076 01382$:
      005AE5 90 06 8B         [24] 2077 	mov	dptr,#_D0UsbConfig
      005AE8 E0               [24] 2078 	movx	a,@dptr
      005AE9 70 03            [24] 2079 	jnz	01383$
      005AEB 02 5D 4F         [24] 2080 	ljmp	00228$
      005AEE                       2081 01383$:
      005AEE 90 06 86         [24] 2082 	mov	dptr,#_D0SetupLen
      005AF1 E0               [24] 2083 	movx	a,@dptr
      005AF2 F8               [12] 2084 	mov	r0,a
      005AF3 A3               [24] 2085 	inc	dptr
      005AF4 E0               [24] 2086 	movx	a,@dptr
      005AF5 48               [12] 2087 	orl	a,r0
      005AF6 70 03            [24] 2088 	jnz	01384$
      005AF8 02 5D 4F         [24] 2089 	ljmp	00228$
      005AFB                       2090 01384$:
                                   2091 ;	tmk_core/protocol/ch555/usb_ak820.c:258: report_id = value;
      005AFB C0 03            [24] 2092 	push	ar3
      005AFD C0 04            [24] 2093 	push	ar4
      005AFF 8D 01            [24] 2094 	mov	ar1,r5
                                   2095 ;	tmk_core/protocol/ch555/usb_ak820.c:259: if ((value >> 8) == 1 && index == KEYBOARD_INTERFACE && !report_id) {
      005B01 8E 00            [24] 2096 	mov	ar0,r6
      005B03 B8 01 03         [24] 2097 	cjne	r0,#0x01,01385$
      005B06 E8               [12] 2098 	mov	a,r0
      005B07 80 01            [24] 2099 	sjmp	01386$
      005B09                       2100 01385$:
      005B09 E4               [12] 2101 	clr	a
      005B0A                       2102 01386$:
      005B0A F5 24            [12] 2103 	mov	_control_setup_sloc1_1_0,a
      005B0C D0 04            [24] 2104 	pop	ar4
      005B0E D0 03            [24] 2105 	pop	ar3
      005B10 E5 24            [12] 2106 	mov	a,_control_setup_sloc1_1_0
      005B12 60 17            [24] 2107 	jz	00160$
      005B14 EB               [12] 2108 	mov	a,r3
      005B15 4C               [12] 2109 	orl	a,r4
      005B16 70 13            [24] 2110 	jnz	00160$
      005B18 E9               [12] 2111 	mov	a,r1
      005B19 70 10            [24] 2112 	jnz	00160$
                                   2113 ;	tmk_core/protocol/ch555/usb_ak820.c:260: length = KEYBOARD_EPSIZE;
      005B1B 90 06 EE         [24] 2114 	mov	dptr,#_control_setup_length_10000_286
      005B1E 74 08            [12] 2115 	mov	a,#0x08
      005B20 F0               [24] 2116 	movx	@dptr,a
      005B21 E4               [12] 2117 	clr	a
      005B22 A3               [24] 2118 	inc	dptr
      005B23 F0               [24] 2119 	movx	@dptr,a
                                   2120 ;	tmk_core/protocol/ch555/usb_ak820.c:261: offset = SNAPSHOT_KEYBOARD;
      005B24 90 06 F0         [24] 2121 	mov	dptr,#_control_setup_offset_10000_286
      005B27 F0               [24] 2122 	movx	@dptr,a
      005B28 02 5C AF         [24] 2123 	ljmp	00161$
      005B2B                       2124 00160$:
                                   2125 ;	tmk_core/protocol/ch555/usb_ak820.c:262: } else if ((value >> 8) == 1 && index == SHARED_INTERFACE &&
      005B2B E5 24            [12] 2126 	mov	a,_control_setup_sloc1_1_0
      005B2D 60 27            [24] 2127 	jz	00154$
      005B2F BB 02 24         [24] 2128 	cjne	r3,#0x02,00154$
      005B32 BC 00 21         [24] 2129 	cjne	r4,#0x00,00154$
                                   2130 ;	tmk_core/protocol/ch555/usb_ak820.c:263: report_id < sizeof(shared_lengths) && shared_lengths[report_id]) {
      005B35 B9 07 00         [24] 2131 	cjne	r1,#0x07,01393$
      005B38                       2132 01393$:
      005B38 50 1C            [24] 2133 	jnc	00154$
      005B3A E9               [12] 2134 	mov	a,r1
      005B3B 90 B6 19         [24] 2135 	mov	dptr,#_shared_lengths
      005B3E 93               [24] 2136 	movc	a,@a+dptr
      005B3F F8               [12] 2137 	mov	r0,a
      005B40 60 14            [24] 2138 	jz	00154$
                                   2139 ;	tmk_core/protocol/ch555/usb_ak820.c:264: length = shared_lengths[report_id];
      005B42 90 06 EE         [24] 2140 	mov	dptr,#_control_setup_length_10000_286
      005B45 E8               [12] 2141 	mov	a,r0
      005B46 F0               [24] 2142 	movx	@dptr,a
      005B47 E4               [12] 2143 	clr	a
      005B48 A3               [24] 2144 	inc	dptr
      005B49 F0               [24] 2145 	movx	@dptr,a
                                   2146 ;	tmk_core/protocol/ch555/usb_ak820.c:265: offset = shared_offsets[report_id];
      005B4A E9               [12] 2147 	mov	a,r1
      005B4B 90 B6 12         [24] 2148 	mov	dptr,#_shared_offsets
      005B4E 93               [24] 2149 	movc	a,@a+dptr
      005B4F 90 06 F0         [24] 2150 	mov	dptr,#_control_setup_offset_10000_286
      005B52 F0               [24] 2151 	movx	@dptr,a
      005B53 02 5C AF         [24] 2152 	ljmp	00161$
      005B56                       2153 00154$:
                                   2154 ;	tmk_core/protocol/ch555/usb_ak820.c:266: } else if ((value >> 8) == 1 && index == RAW_INTERFACE && !report_id) {
      005B56 E5 24            [12] 2155 	mov	a,_control_setup_sloc1_1_0
      005B58 60 7A            [24] 2156 	jz	00149$
      005B5A BB 01 77         [24] 2157 	cjne	r3,#0x01,00149$
      005B5D BC 00 74         [24] 2158 	cjne	r4,#0x00,00149$
      005B60 E9               [12] 2159 	mov	a,r1
      005B61 70 71            [24] 2160 	jnz	00149$
                                   2161 ;	tmk_core/protocol/ch555/usb_ak820.c:267: length = D0SetupLen < RAW_EPSIZE ? D0SetupLen : RAW_EPSIZE;
      005B63 90 06 86         [24] 2162 	mov	dptr,#_D0SetupLen
      005B66 E0               [24] 2163 	movx	a,@dptr
      005B67 F8               [12] 2164 	mov	r0,a
      005B68 A3               [24] 2165 	inc	dptr
      005B69 E0               [24] 2166 	movx	a,@dptr
      005B6A F9               [12] 2167 	mov	r1,a
      005B6B C3               [12] 2168 	clr	c
      005B6C E8               [12] 2169 	mov	a,r0
      005B6D 94 20            [12] 2170 	subb	a,#0x20
      005B6F E9               [12] 2171 	mov	a,r1
      005B70 94 00            [12] 2172 	subb	a,#0x00
      005B72 50 0A            [24] 2173 	jnc	00320$
      005B74 90 06 86         [24] 2174 	mov	dptr,#_D0SetupLen
      005B77 E0               [24] 2175 	movx	a,@dptr
      005B78 F8               [12] 2176 	mov	r0,a
      005B79 A3               [24] 2177 	inc	dptr
      005B7A E0               [24] 2178 	movx	a,@dptr
      005B7B F9               [12] 2179 	mov	r1,a
      005B7C 80 04            [24] 2180 	sjmp	00321$
      005B7E                       2181 00320$:
      005B7E 78 20            [12] 2182 	mov	r0,#0x20
      005B80 79 00            [12] 2183 	mov	r1,#0x00
      005B82                       2184 00321$:
                                   2185 ;	tmk_core/protocol/ch555/usb_ak820.c:268: for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = pUSB_BUF_DEV0[UX_EP3_ADDR + i];
      005B82 75 24 00         [24] 2186 	mov	_control_setup_sloc1_1_0,#0x00
      005B85                       2187 00293$:
      005B85 C0 03            [24] 2188 	push	ar3
      005B87 C0 04            [24] 2189 	push	ar4
      005B89 AB 24            [24] 2190 	mov	r3,_control_setup_sloc1_1_0
      005B8B 7C 00            [12] 2191 	mov	r4,#0x00
      005B8D C3               [12] 2192 	clr	c
      005B8E EB               [12] 2193 	mov	a,r3
      005B8F 98               [12] 2194 	subb	a,r0
      005B90 EC               [12] 2195 	mov	a,r4
      005B91 99               [12] 2196 	subb	a,r1
      005B92 D0 04            [24] 2197 	pop	ar4
      005B94 D0 03            [24] 2198 	pop	ar3
      005B96 50 32            [24] 2199 	jnc	00131$
      005B98 C0 00            [24] 2200 	push	ar0
      005B9A C0 01            [24] 2201 	push	ar1
      005B9C 85 24 26         [24] 2202 	mov	_control_setup_sloc2_1_0,_control_setup_sloc1_1_0
      005B9F 74 10            [12] 2203 	mov	a,#0x10
      005BA1 24 00            [12] 2204 	add	a, #0x00
      005BA3 F5 27            [12] 2205 	mov	(_control_setup_sloc2_1_0 + 1),a
      005BA5 A8 24            [24] 2206 	mov	r0,_control_setup_sloc1_1_0
      005BA7 79 00            [12] 2207 	mov	r1,#0x00
      005BA9 74 C0            [12] 2208 	mov	a,#0xc0
      005BAB 28               [12] 2209 	add	a, r0
      005BAC F8               [12] 2210 	mov	r0,a
      005BAD E4               [12] 2211 	clr	a
      005BAE 39               [12] 2212 	addc	a, r1
      005BAF F9               [12] 2213 	mov	r1,a
      005BB0 88 82            [24] 2214 	mov	dpl,r0
      005BB2 74 10            [12] 2215 	mov	a,#0x10
      005BB4 29               [12] 2216 	add	a, r1
      005BB5 F5 83            [12] 2217 	mov	dph,a
      005BB7 E0               [24] 2218 	movx	a,@dptr
      005BB8 85 26 82         [24] 2219 	mov	dpl,_control_setup_sloc2_1_0
      005BBB 85 27 83         [24] 2220 	mov	dph,(_control_setup_sloc2_1_0 + 1)
      005BBE F0               [24] 2221 	movx	@dptr,a
      005BBF E5 24            [12] 2222 	mov	a,_control_setup_sloc1_1_0
      005BC1 04               [12] 2223 	inc	a
      005BC2 F5 24            [12] 2224 	mov	_control_setup_sloc1_1_0,a
      005BC4 D0 01            [24] 2225 	pop	ar1
      005BC6 D0 00            [24] 2226 	pop	ar0
      005BC8 80 BB            [24] 2227 	sjmp	00293$
      005BCA                       2228 00131$:
                                   2229 ;	tmk_core/protocol/ch555/usb_ak820.c:269: length = 0; /* data already copied */
      005BCA 90 06 EE         [24] 2230 	mov	dptr,#_control_setup_length_10000_286
      005BCD E4               [12] 2231 	clr	a
      005BCE F0               [24] 2232 	movx	@dptr,a
      005BCF A3               [24] 2233 	inc	dptr
      005BD0 F0               [24] 2234 	movx	@dptr,a
      005BD1 02 5C AF         [24] 2235 	ljmp	00161$
      005BD4                       2236 00149$:
                                   2237 ;	tmk_core/protocol/ch555/usb_ak820.c:270: } else if (value == 0x0200 && index == KEYBOARD_INTERFACE) {
      005BD4 8D 00            [24] 2238 	mov	ar0,r5
      005BD6 8E 01            [24] 2239 	mov	ar1,r6
      005BD8 B8 00 21         [24] 2240 	cjne	r0,#0x00,00145$
      005BDB B9 02 1E         [24] 2241 	cjne	r1,#0x02,00145$
      005BDE EB               [12] 2242 	mov	a,r3
      005BDF 4C               [12] 2243 	orl	a,r4
      005BE0 70 1A            [24] 2244 	jnz	00145$
                                   2245 ;	tmk_core/protocol/ch555/usb_ak820.c:271: pD0_EP0_BUF[0] = KB_USB_SetReport;
      005BE2 90 06 90         [24] 2246 	mov	dptr,#_KB_USB_SetReport
      005BE5 E0               [24] 2247 	movx	a,@dptr
      005BE6 90 10 00         [24] 2248 	mov	dptr,#0x1000
      005BE9 F0               [24] 2249 	movx	@dptr,a
                                   2250 ;	tmk_core/protocol/ch555/usb_ak820.c:272: length = 0;
      005BEA 90 06 EE         [24] 2251 	mov	dptr,#_control_setup_length_10000_286
      005BED E4               [12] 2252 	clr	a
      005BEE F0               [24] 2253 	movx	@dptr,a
      005BEF A3               [24] 2254 	inc	dptr
      005BF0 F0               [24] 2255 	movx	@dptr,a
                                   2256 ;	tmk_core/protocol/ch555/usb_ak820.c:273: D0SetupLen = 1;
      005BF1 90 06 86         [24] 2257 	mov	dptr,#_D0SetupLen
      005BF4 04               [12] 2258 	inc	a
      005BF5 F0               [24] 2259 	movx	@dptr,a
      005BF6 E4               [12] 2260 	clr	a
      005BF7 A3               [24] 2261 	inc	dptr
      005BF8 F0               [24] 2262 	movx	@dptr,a
      005BF9 02 5C AF         [24] 2263 	ljmp	00161$
      005BFC                       2264 00145$:
                                   2265 ;	tmk_core/protocol/ch555/usb_ak820.c:274: } else if (value == (0x0200 | REPORT_ID_NKRO) && index == SHARED_INTERFACE) {
      005BFC B8 06 41         [24] 2266 	cjne	r0,#0x06,00141$
      005BFF B9 02 3E         [24] 2267 	cjne	r1,#0x02,00141$
      005C02 BB 02 3B         [24] 2268 	cjne	r3,#0x02,00141$
      005C05 BC 00 38         [24] 2269 	cjne	r4,#0x00,00141$
                                   2270 ;	tmk_core/protocol/ch555/usb_ak820.c:275: pD0_EP0_BUF[0] = REPORT_ID_NKRO;
      005C08 C0 03            [24] 2271 	push	ar3
      005C0A C0 04            [24] 2272 	push	ar4
      005C0C 90 10 00         [24] 2273 	mov	dptr,#0x1000
      005C0F 74 06            [12] 2274 	mov	a,#0x06
      005C11 F0               [24] 2275 	movx	@dptr,a
                                   2276 ;	tmk_core/protocol/ch555/usb_ak820.c:276: pD0_EP0_BUF[1] = KB_USB_SetReport;
      005C12 90 06 90         [24] 2277 	mov	dptr,#_KB_USB_SetReport
      005C15 E0               [24] 2278 	movx	a,@dptr
      005C16 90 10 01         [24] 2279 	mov	dptr,#0x1001
      005C19 F0               [24] 2280 	movx	@dptr,a
                                   2281 ;	tmk_core/protocol/ch555/usb_ak820.c:277: length = 0;
      005C1A 90 06 EE         [24] 2282 	mov	dptr,#_control_setup_length_10000_286
      005C1D E4               [12] 2283 	clr	a
      005C1E F0               [24] 2284 	movx	@dptr,a
      005C1F A3               [24] 2285 	inc	dptr
      005C20 F0               [24] 2286 	movx	@dptr,a
                                   2287 ;	tmk_core/protocol/ch555/usb_ak820.c:278: if (D0SetupLen > 2) D0SetupLen = 2;
      005C21 90 06 86         [24] 2288 	mov	dptr,#_D0SetupLen
      005C24 E0               [24] 2289 	movx	a,@dptr
      005C25 FB               [12] 2290 	mov	r3,a
      005C26 A3               [24] 2291 	inc	dptr
      005C27 E0               [24] 2292 	movx	a,@dptr
      005C28 FC               [12] 2293 	mov	r4,a
      005C29 C3               [12] 2294 	clr	c
      005C2A 74 02            [12] 2295 	mov	a,#0x02
      005C2C 9B               [12] 2296 	subb	a,r3
      005C2D E4               [12] 2297 	clr	a
      005C2E 9C               [12] 2298 	subb	a,r4
      005C2F D0 04            [24] 2299 	pop	ar4
      005C31 D0 03            [24] 2300 	pop	ar3
      005C33 50 7A            [24] 2301 	jnc	00161$
                                   2302 ;	free result
      005C35 90 06 86         [24] 2303 	mov	dptr,#_D0SetupLen
      005C38 74 02            [12] 2304 	mov	a,#0x02
      005C3A F0               [24] 2305 	movx	@dptr,a
      005C3B E4               [12] 2306 	clr	a
      005C3C A3               [24] 2307 	inc	dptr
      005C3D F0               [24] 2308 	movx	@dptr,a
      005C3E 80 6F            [24] 2309 	sjmp	00161$
      005C40                       2310 00141$:
                                   2311 ;	tmk_core/protocol/ch555/usb_ak820.c:279: } else if (value == 0x0300 && index == RAW_INTERFACE) {
      005C40 B8 00 69         [24] 2312 	cjne	r0,#0x00,00137$
      005C43 B9 03 66         [24] 2313 	cjne	r1,#0x03,00137$
      005C46 BB 01 63         [24] 2314 	cjne	r3,#0x01,00137$
      005C49 BC 00 60         [24] 2315 	cjne	r4,#0x00,00137$
                                   2316 ;	tmk_core/protocol/ch555/usb_ak820.c:282: pD0_EP0_BUF[0] = 'A';
      005C4C 90 10 00         [24] 2317 	mov	dptr,#0x1000
      005C4F 74 41            [12] 2318 	mov	a,#0x41
      005C51 F0               [24] 2319 	movx	@dptr,a
                                   2320 ;	tmk_core/protocol/ch555/usb_ak820.c:283: pD0_EP0_BUF[1] = 'K';
      005C52 A3               [24] 2321 	inc	dptr
      005C53 74 4B            [12] 2322 	mov	a,#0x4b
      005C55 F0               [24] 2323 	movx	@dptr,a
                                   2324 ;	tmk_core/protocol/ch555/usb_ak820.c:284: pD0_EP0_BUF[2] = 'B';
      005C56 A3               [24] 2325 	inc	dptr
      005C57 74 42            [12] 2326 	mov	a,#0x42
      005C59 F0               [24] 2327 	movx	@dptr,a
                                   2328 ;	tmk_core/protocol/ch555/usb_ak820.c:285: pD0_EP0_BUF[3] = 'T';
      005C5A A3               [24] 2329 	inc	dptr
      005C5B 74 54            [12] 2330 	mov	a,#0x54
      005C5D F0               [24] 2331 	movx	@dptr,a
                                   2332 ;	tmk_core/protocol/ch555/usb_ak820.c:286: pD0_EP0_BUF[4] = 1;
      005C5E A3               [24] 2333 	inc	dptr
      005C5F 74 01            [12] 2334 	mov	a,#0x01
      005C61 F0               [24] 2335 	movx	@dptr,a
                                   2336 ;	tmk_core/protocol/ch555/usb_ak820.c:287: pD0_EP0_BUF[5] = ak820_boot_stage;
      005C62 90 06 91         [24] 2337 	mov	dptr,#_ak820_boot_stage
      005C65 E0               [24] 2338 	movx	a,@dptr
      005C66 90 10 05         [24] 2339 	mov	dptr,#0x1005
      005C69 F0               [24] 2340 	movx	@dptr,a
                                   2341 ;	tmk_core/protocol/ch555/usb_ak820.c:288: pD0_EP0_BUF[6] = ak820_main_heartbeat;
      005C6A 90 06 92         [24] 2342 	mov	dptr,#_ak820_main_heartbeat
      005C6D E0               [24] 2343 	movx	a,@dptr
      005C6E 90 10 06         [24] 2344 	mov	dptr,#0x1006
      005C71 F0               [24] 2345 	movx	@dptr,a
                                   2346 ;	tmk_core/protocol/ch555/usb_ak820.c:289: pD0_EP0_BUF[7] = (USB_EnumStatus ? 1 : 0) | (USB_SleepStatus & 2);
      005C72 90 06 8C         [24] 2347 	mov	dptr,#_USB_EnumStatus
      005C75 E0               [24] 2348 	movx	a,@dptr
      005C76 60 02            [24] 2349 	jz	00322$
      005C78 74 01            [12] 2350 	mov	a,#0x01
      005C7A                       2351 00322$:
      005C7A F9               [12] 2352 	mov	r1,a
      005C7B 90 06 8D         [24] 2353 	mov	dptr,#_USB_SleepStatus
      005C7E E0               [24] 2354 	movx	a,@dptr
      005C7F 54 02            [12] 2355 	anl	a,#0x02
      005C81 F8               [12] 2356 	mov	r0,a
      005C82 E9               [12] 2357 	mov	a,r1
      005C83 42 00            [12] 2358 	orl	ar0,a
      005C85 90 10 07         [24] 2359 	mov	dptr,#0x1007
      005C88 E8               [12] 2360 	mov	a,r0
      005C89 F0               [24] 2361 	movx	@dptr,a
                                   2362 ;	tmk_core/protocol/ch555/usb_ak820.c:290: length = 0;
      005C8A 90 06 EE         [24] 2363 	mov	dptr,#_control_setup_length_10000_286
      005C8D E4               [12] 2364 	clr	a
      005C8E F0               [24] 2365 	movx	@dptr,a
      005C8F A3               [24] 2366 	inc	dptr
      005C90 F0               [24] 2367 	movx	@dptr,a
                                   2368 ;	tmk_core/protocol/ch555/usb_ak820.c:291: if (D0SetupLen > 8) D0SetupLen = 8;
      005C91 90 06 86         [24] 2369 	mov	dptr,#_D0SetupLen
      005C94 E0               [24] 2370 	movx	a,@dptr
      005C95 F8               [12] 2371 	mov	r0,a
      005C96 A3               [24] 2372 	inc	dptr
      005C97 E0               [24] 2373 	movx	a,@dptr
      005C98 F9               [12] 2374 	mov	r1,a
      005C99 C3               [12] 2375 	clr	c
      005C9A 74 08            [12] 2376 	mov	a,#0x08
      005C9C 98               [12] 2377 	subb	a,r0
      005C9D E4               [12] 2378 	clr	a
      005C9E 99               [12] 2379 	subb	a,r1
      005C9F 50 0E            [24] 2380 	jnc	00161$
                                   2381 ;	free result
      005CA1 90 06 86         [24] 2382 	mov	dptr,#_D0SetupLen
      005CA4 74 08            [12] 2383 	mov	a,#0x08
      005CA6 F0               [24] 2384 	movx	@dptr,a
      005CA7 E4               [12] 2385 	clr	a
      005CA8 A3               [24] 2386 	inc	dptr
      005CA9 F0               [24] 2387 	movx	@dptr,a
      005CAA 80 03            [24] 2388 	sjmp	00161$
      005CAC                       2389 00137$:
                                   2390 ;	tmk_core/protocol/ch555/usb_ak820.c:292: } else { control_stall(); return; }
      005CAC 02 54 8E         [24] 2391 	ljmp	_control_stall
      005CAF                       2392 00161$:
                                   2393 ;	tmk_core/protocol/ch555/usb_ak820.c:293: if (length) {
      005CAF 90 06 EE         [24] 2394 	mov	dptr,#_control_setup_length_10000_286
      005CB2 E0               [24] 2395 	movx	a,@dptr
      005CB3 F5 26            [12] 2396 	mov	_control_setup_sloc2_1_0,a
      005CB5 A3               [24] 2397 	inc	dptr
      005CB6 E0               [24] 2398 	movx	a,@dptr
      005CB7 F5 27            [12] 2399 	mov	(_control_setup_sloc2_1_0 + 1),a
      005CB9 E5 26            [12] 2400 	mov	a,_control_setup_sloc2_1_0
      005CBB 45 27            [12] 2401 	orl	a,(_control_setup_sloc2_1_0 + 1)
      005CBD 60 60            [24] 2402 	jz	00171$
                                   2403 ;	tmk_core/protocol/ch555/usb_ak820.c:294: if (D0SetupLen > length) D0SetupLen = length;
      005CBF 90 06 86         [24] 2404 	mov	dptr,#_D0SetupLen
      005CC2 E0               [24] 2405 	movx	a,@dptr
      005CC3 F8               [12] 2406 	mov	r0,a
      005CC4 A3               [24] 2407 	inc	dptr
      005CC5 E0               [24] 2408 	movx	a,@dptr
      005CC6 F9               [12] 2409 	mov	r1,a
      005CC7 C3               [12] 2410 	clr	c
      005CC8 E5 26            [12] 2411 	mov	a,_control_setup_sloc2_1_0
      005CCA 98               [12] 2412 	subb	a,r0
      005CCB E5 27            [12] 2413 	mov	a,(_control_setup_sloc2_1_0 + 1)
      005CCD 99               [12] 2414 	subb	a,r1
      005CCE 50 0A            [24] 2415 	jnc	00555$
                                   2416 ;	free result
      005CD0 90 06 86         [24] 2417 	mov	dptr,#_D0SetupLen
      005CD3 E5 26            [12] 2418 	mov	a,_control_setup_sloc2_1_0
      005CD5 F0               [24] 2419 	movx	@dptr,a
      005CD6 E5 27            [12] 2420 	mov	a,(_control_setup_sloc2_1_0 + 1)
      005CD8 A3               [24] 2421 	inc	dptr
      005CD9 F0               [24] 2422 	movx	@dptr,a
                                   2423 ;	tmk_core/protocol/ch555/usb_ak820.c:295: for (i = 0; i < D0SetupLen; ++i) pD0_EP0_BUF[i] = input_snapshot[offset + i];
      005CDA                       2424 00555$:
      005CDA 90 06 F0         [24] 2425 	mov	dptr,#_control_setup_offset_10000_286
      005CDD E0               [24] 2426 	movx	a,@dptr
      005CDE F5 28            [12] 2427 	mov	_control_setup_sloc3_1_0,a
      005CE0 75 26 00         [24] 2428 	mov	_control_setup_sloc2_1_0,#0x00
      005CE3                       2429 00296$:
      005CE3 90 06 86         [24] 2430 	mov	dptr,#_D0SetupLen
      005CE6 E0               [24] 2431 	movx	a,@dptr
      005CE7 F5 24            [12] 2432 	mov	_control_setup_sloc1_1_0,a
      005CE9 A3               [24] 2433 	inc	dptr
      005CEA E0               [24] 2434 	movx	a,@dptr
      005CEB F5 25            [12] 2435 	mov	(_control_setup_sloc1_1_0 + 1),a
      005CED A8 26            [24] 2436 	mov	r0,_control_setup_sloc2_1_0
      005CEF 79 00            [12] 2437 	mov	r1,#0x00
      005CF1 C3               [12] 2438 	clr	c
      005CF2 E8               [12] 2439 	mov	a,r0
      005CF3 95 24            [12] 2440 	subb	a,_control_setup_sloc1_1_0
      005CF5 E9               [12] 2441 	mov	a,r1
      005CF6 95 25            [12] 2442 	subb	a,(_control_setup_sloc1_1_0 + 1)
      005CF8 50 44            [24] 2443 	jnc	00172$
      005CFA 85 26 24         [24] 2444 	mov	_control_setup_sloc1_1_0,_control_setup_sloc2_1_0
      005CFD 74 10            [12] 2445 	mov	a,#0x10
      005CFF 24 00            [12] 2446 	add	a, #0x00
      005D01 F5 25            [12] 2447 	mov	(_control_setup_sloc1_1_0 + 1),a
      005D03 E5 26            [12] 2448 	mov	a,_control_setup_sloc2_1_0
      005D05 25 28            [12] 2449 	add	a, _control_setup_sloc3_1_0
      005D07 24 B6            [12] 2450 	add	a, #_input_snapshot
      005D09 F5 82            [12] 2451 	mov	dpl,a
      005D0B E4               [12] 2452 	clr	a
      005D0C 34 06            [12] 2453 	addc	a,#(_input_snapshot >> 8)
      005D0E F5 83            [12] 2454 	mov	dph,a
      005D10 E0               [24] 2455 	movx	a,@dptr
      005D11 85 24 82         [24] 2456 	mov	dpl,_control_setup_sloc1_1_0
      005D14 85 25 83         [24] 2457 	mov	dph,(_control_setup_sloc1_1_0 + 1)
      005D17 F0               [24] 2458 	movx	@dptr,a
      005D18 E5 26            [12] 2459 	mov	a,_control_setup_sloc2_1_0
      005D1A 04               [12] 2460 	inc	a
      005D1B F5 26            [12] 2461 	mov	_control_setup_sloc2_1_0,a
      005D1D 80 C4            [24] 2462 	sjmp	00296$
      005D1F                       2463 00171$:
                                   2464 ;	tmk_core/protocol/ch555/usb_ak820.c:296: } else if (index == RAW_INTERFACE && D0SetupLen > RAW_EPSIZE) D0SetupLen = RAW_EPSIZE;
      005D1F BB 01 1C         [24] 2465 	cjne	r3,#0x01,00172$
      005D22 BC 00 19         [24] 2466 	cjne	r4,#0x00,00172$
      005D25 90 06 86         [24] 2467 	mov	dptr,#_D0SetupLen
      005D28 E0               [24] 2468 	movx	a,@dptr
      005D29 F8               [12] 2469 	mov	r0,a
      005D2A A3               [24] 2470 	inc	dptr
      005D2B E0               [24] 2471 	movx	a,@dptr
      005D2C F9               [12] 2472 	mov	r1,a
      005D2D C3               [12] 2473 	clr	c
      005D2E 74 20            [12] 2474 	mov	a,#0x20
      005D30 98               [12] 2475 	subb	a,r0
      005D31 E4               [12] 2476 	clr	a
      005D32 99               [12] 2477 	subb	a,r1
      005D33 50 09            [24] 2478 	jnc	00172$
                                   2479 ;	free result
      005D35 90 06 86         [24] 2480 	mov	dptr,#_D0SetupLen
      005D38 74 20            [12] 2481 	mov	a,#0x20
      005D3A F0               [24] 2482 	movx	@dptr,a
      005D3B E4               [12] 2483 	clr	a
      005D3C A3               [24] 2484 	inc	dptr
      005D3D F0               [24] 2485 	movx	@dptr,a
      005D3E                       2486 00172$:
                                   2487 ;	tmk_core/protocol/ch555/usb_ak820.c:297: D0_EP0T_L = D0SetupLen;
      005D3E 90 06 86         [24] 2488 	mov	dptr,#_D0SetupLen
      005D41 E0               [24] 2489 	movx	a,@dptr
      005D42 90 22 08         [24] 2490 	mov	dptr,#0x2208
      005D45 F0               [24] 2491 	movx	@dptr,a
                                   2492 ;	tmk_core/protocol/ch555/usb_ak820.c:298: control_phase = CTRL_STATUS_OUT;
      005D46 90 06 E4         [24] 2493 	mov	dptr,#_control_phase
      005D49 74 02            [12] 2494 	mov	a,#0x02
      005D4B F0               [24] 2495 	movx	@dptr,a
      005D4C 02 5E F9         [24] 2496 	ljmp	00287$
      005D4F                       2497 00228$:
                                   2498 ;	tmk_core/protocol/ch555/usb_ak820.c:299: } else if (type == 0x21 && D0SetupReqCode == HID_SET_REPORT && D0UsbConfig) {
      005D4F E4               [12] 2499 	clr	a
      005D50 BF 21 01         [24] 2500 	cjne	r7,#0x21,01422$
      005D53 04               [12] 2501 	inc	a
      005D54                       2502 01422$:
      005D54 FF               [12] 2503 	mov	r7,a
      005D55 70 03            [24] 2504 	jnz	01424$
      005D57 02 5D F9         [24] 2505 	ljmp	00223$
      005D5A                       2506 01424$:
      005D5A 90 06 85         [24] 2507 	mov	dptr,#_D0SetupReqCode
      005D5D E0               [24] 2508 	movx	a,@dptr
      005D5E F9               [12] 2509 	mov	r1,a
      005D5F B9 09 02         [24] 2510 	cjne	r1,#0x09,01425$
      005D62 80 03            [24] 2511 	sjmp	01426$
      005D64                       2512 01425$:
      005D64 02 5D F9         [24] 2513 	ljmp	00223$
      005D67                       2514 01426$:
      005D67 90 06 8B         [24] 2515 	mov	dptr,#_D0UsbConfig
      005D6A E0               [24] 2516 	movx	a,@dptr
      005D6B 70 03            [24] 2517 	jnz	01427$
      005D6D 02 5D F9         [24] 2518 	ljmp	00223$
      005D70                       2519 01427$:
                                   2520 ;	tmk_core/protocol/ch555/usb_ak820.c:300: if (index == RAW_INTERFACE && value == 0x0200 && D0SetupLen == RAW_EPSIZE && raw_state == RAW_IDLE) {
      005D70 BB 01 2D         [24] 2521 	cjne	r3,#0x01,00184$
      005D73 BC 00 2A         [24] 2522 	cjne	r4,#0x00,00184$
      005D76 8D 00            [24] 2523 	mov	ar0,r5
      005D78 8E 01            [24] 2524 	mov	ar1,r6
      005D7A B8 00 23         [24] 2525 	cjne	r0,#0x00,00184$
      005D7D B9 02 20         [24] 2526 	cjne	r1,#0x02,00184$
      005D80 90 06 86         [24] 2527 	mov	dptr,#_D0SetupLen
      005D83 E0               [24] 2528 	movx	a,@dptr
      005D84 F8               [12] 2529 	mov	r0,a
      005D85 A3               [24] 2530 	inc	dptr
      005D86 E0               [24] 2531 	movx	a,@dptr
      005D87 F9               [12] 2532 	mov	r1,a
      005D88 B8 20 15         [24] 2533 	cjne	r0,#0x20,00184$
      005D8B B9 00 12         [24] 2534 	cjne	r1,#0x00,00184$
      005D8E 90 06 93         [24] 2535 	mov	dptr,#_raw_state
      005D91 E0               [24] 2536 	movx	a,@dptr
      005D92 70 0C            [24] 2537 	jnz	00184$
                                   2538 ;	tmk_core/protocol/ch555/usb_ak820.c:301: raw_state = RAW_RX;
      005D94 90 06 93         [24] 2539 	mov	dptr,#_raw_state
      005D97 74 01            [12] 2540 	mov	a,#0x01
      005D99 F0               [24] 2541 	movx	@dptr,a
                                   2542 ;	tmk_core/protocol/ch555/usb_ak820.c:302: output_kind = OUTPUT_RAW;
      005D9A 90 06 E5         [24] 2543 	mov	dptr,#_output_kind
      005D9D F0               [24] 2544 	movx	@dptr,a
      005D9E 80 52            [24] 2545 	sjmp	00185$
      005DA0                       2546 00184$:
                                   2547 ;	tmk_core/protocol/ch555/usb_ak820.c:303: } else if (index == KEYBOARD_INTERFACE && value == 0x0200 && D0SetupLen == 1) {
      005DA0 EB               [12] 2548 	mov	a,r3
      005DA1 4C               [12] 2549 	orl	a,r4
      005DA2 70 20            [24] 2550 	jnz	00179$
      005DA4 8D 00            [24] 2551 	mov	ar0,r5
      005DA6 8E 01            [24] 2552 	mov	ar1,r6
      005DA8 B8 00 19         [24] 2553 	cjne	r0,#0x00,00179$
      005DAB B9 02 16         [24] 2554 	cjne	r1,#0x02,00179$
      005DAE 90 06 86         [24] 2555 	mov	dptr,#_D0SetupLen
      005DB1 E0               [24] 2556 	movx	a,@dptr
      005DB2 F8               [12] 2557 	mov	r0,a
      005DB3 A3               [24] 2558 	inc	dptr
      005DB4 E0               [24] 2559 	movx	a,@dptr
      005DB5 F9               [12] 2560 	mov	r1,a
      005DB6 B8 01 0B         [24] 2561 	cjne	r0,#0x01,00179$
      005DB9 B9 00 08         [24] 2562 	cjne	r1,#0x00,00179$
                                   2563 ;	tmk_core/protocol/ch555/usb_ak820.c:304: output_kind = OUTPUT_LED;
      005DBC 90 06 E5         [24] 2564 	mov	dptr,#_output_kind
      005DBF 74 02            [12] 2565 	mov	a,#0x02
      005DC1 F0               [24] 2566 	movx	@dptr,a
      005DC2 80 2E            [24] 2567 	sjmp	00185$
      005DC4                       2568 00179$:
                                   2569 ;	tmk_core/protocol/ch555/usb_ak820.c:306: } else if (index == SHARED_INTERFACE && value == (0x0200 | REPORT_ID_NKRO) && D0SetupLen == 2) {
      005DC4 BB 02 28         [24] 2570 	cjne	r3,#0x02,00174$
      005DC7 BC 00 25         [24] 2571 	cjne	r4,#0x00,00174$
      005DCA 8D 00            [24] 2572 	mov	ar0,r5
      005DCC 8E 01            [24] 2573 	mov	ar1,r6
      005DCE B8 06 1E         [24] 2574 	cjne	r0,#0x06,00174$
      005DD1 B9 02 1B         [24] 2575 	cjne	r1,#0x02,00174$
      005DD4 90 06 86         [24] 2576 	mov	dptr,#_D0SetupLen
      005DD7 E0               [24] 2577 	movx	a,@dptr
      005DD8 F8               [12] 2578 	mov	r0,a
      005DD9 A3               [24] 2579 	inc	dptr
      005DDA E0               [24] 2580 	movx	a,@dptr
      005DDB F9               [12] 2581 	mov	r1,a
      005DDC B8 02 10         [24] 2582 	cjne	r0,#0x02,00174$
      005DDF B9 00 0D         [24] 2583 	cjne	r1,#0x00,00174$
                                   2584 ;	tmk_core/protocol/ch555/usb_ak820.c:307: output_kind = OUTPUT_SHARED_LED;
      005DE2 90 06 E5         [24] 2585 	mov	dptr,#_output_kind
      005DE5 74 03            [12] 2586 	mov	a,#0x03
      005DE7 F0               [24] 2587 	movx	@dptr,a
                                   2588 ;	tmk_core/protocol/ch555/usb_ak820.c:308: output_report_id = REPORT_ID_NKRO;
      005DE8 90 06 E6         [24] 2589 	mov	dptr,#_output_report_id
      005DEB 23               [12] 2590 	rl	a
      005DEC F0               [24] 2591 	movx	@dptr,a
      005DED 80 03            [24] 2592 	sjmp	00185$
      005DEF                       2593 00174$:
                                   2594 ;	tmk_core/protocol/ch555/usb_ak820.c:310: } else { control_stall(); return; }
      005DEF 02 54 8E         [24] 2595 	ljmp	_control_stall
      005DF2                       2596 00185$:
                                   2597 ;	tmk_core/protocol/ch555/usb_ak820.c:311: control_phase = CTRL_DATA_OUT;
      005DF2 90 06 E4         [24] 2598 	mov	dptr,#_control_phase
      005DF5 74 04            [12] 2599 	mov	a,#0x04
      005DF7 F0               [24] 2600 	movx	@dptr,a
                                   2601 ;	tmk_core/protocol/ch555/usb_ak820.c:312: return; /* OUT data must arrive before status-IN becomes ACK */
      005DF8 22               [24] 2602 	ret
      005DF9                       2603 00223$:
                                   2604 ;	tmk_core/protocol/ch555/usb_ak820.c:313: } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0x21 && D0SetupReqCode == DEF_USB_SET_PROTOCOL && !D0SetupLen && value <= 1) {
      005DF9 EB               [12] 2605 	mov	a,r3
      005DFA 4C               [12] 2606 	orl	a,r4
      005DFB 70 3B            [24] 2607 	jnz	00215$
      005DFD 90 06 8B         [24] 2608 	mov	dptr,#_D0UsbConfig
      005E00 E0               [24] 2609 	movx	a,@dptr
      005E01 60 35            [24] 2610 	jz	00215$
      005E03 EF               [12] 2611 	mov	a,r7
      005E04 60 32            [24] 2612 	jz	00215$
      005E06 90 06 85         [24] 2613 	mov	dptr,#_D0SetupReqCode
      005E09 E0               [24] 2614 	movx	a,@dptr
      005E0A F9               [12] 2615 	mov	r1,a
      005E0B B9 0B 2A         [24] 2616 	cjne	r1,#0x0b,00215$
      005E0E 90 06 86         [24] 2617 	mov	dptr,#_D0SetupLen
      005E11 E0               [24] 2618 	movx	a,@dptr
      005E12 F8               [12] 2619 	mov	r0,a
      005E13 A3               [24] 2620 	inc	dptr
      005E14 E0               [24] 2621 	movx	a,@dptr
      005E15 48               [12] 2622 	orl	a,r0
      005E16 70 20            [24] 2623 	jnz	00215$
      005E18 8D 00            [24] 2624 	mov	ar0,r5
      005E1A 8E 01            [24] 2625 	mov	ar1,r6
      005E1C C3               [12] 2626 	clr	c
      005E1D 74 01            [12] 2627 	mov	a,#0x01
      005E1F 98               [12] 2628 	subb	a,r0
      005E20 E4               [12] 2629 	clr	a
      005E21 99               [12] 2630 	subb	a,r1
      005E22 40 14            [24] 2631 	jc	00215$
                                   2632 ;	free result
                                   2633 ;	tmk_core/protocol/ch555/usb_ak820.c:314: keyboard_protocol = value;
      005E24 90 0B 9D         [24] 2634 	mov	dptr,#_keyboard_protocol
      005E27 ED               [12] 2635 	mov	a,r5
      005E28 F0               [24] 2636 	movx	@dptr,a
                                   2637 ;	tmk_core/protocol/ch555/usb_ak820.c:315: keyboard_reset = 1;
      005E29 90 06 B5         [24] 2638 	mov	dptr,#_keyboard_reset
      005E2C 74 01            [12] 2639 	mov	a,#0x01
      005E2E F0               [24] 2640 	movx	@dptr,a
                                   2641 ;	tmk_core/protocol/ch555/usb_ak820.c:316: control_phase = CTRL_STATUS_IN;
      005E2F 90 06 E4         [24] 2642 	mov	dptr,#_control_phase
      005E32 74 03            [12] 2643 	mov	a,#0x03
      005E34 F0               [24] 2644 	movx	@dptr,a
      005E35 02 5E F9         [24] 2645 	ljmp	00287$
      005E38                       2646 00215$:
                                   2647 ;	tmk_core/protocol/ch555/usb_ak820.c:317: } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0xa1 && D0SetupReqCode == DEF_USB_GET_PROTOCOL && !value && D0SetupLen == 1) {
      005E38 EB               [12] 2648 	mov	a,r3
      005E39 4C               [12] 2649 	orl	a,r4
      005E3A 70 39            [24] 2650 	jnz	00207$
      005E3C 90 06 8B         [24] 2651 	mov	dptr,#_D0UsbConfig
      005E3F E0               [24] 2652 	movx	a,@dptr
      005E40 60 33            [24] 2653 	jz	00207$
      005E42 EA               [12] 2654 	mov	a,r2
      005E43 60 30            [24] 2655 	jz	00207$
      005E45 90 06 85         [24] 2656 	mov	dptr,#_D0SetupReqCode
      005E48 E0               [24] 2657 	movx	a,@dptr
      005E49 F9               [12] 2658 	mov	r1,a
      005E4A B9 03 28         [24] 2659 	cjne	r1,#0x03,00207$
      005E4D ED               [12] 2660 	mov	a,r5
      005E4E 4E               [12] 2661 	orl	a,r6
      005E4F 70 24            [24] 2662 	jnz	00207$
      005E51 90 06 86         [24] 2663 	mov	dptr,#_D0SetupLen
      005E54 E0               [24] 2664 	movx	a,@dptr
      005E55 F8               [12] 2665 	mov	r0,a
      005E56 A3               [24] 2666 	inc	dptr
      005E57 E0               [24] 2667 	movx	a,@dptr
      005E58 F9               [12] 2668 	mov	r1,a
      005E59 B8 01 19         [24] 2669 	cjne	r0,#0x01,00207$
      005E5C B9 00 16         [24] 2670 	cjne	r1,#0x00,00207$
                                   2671 ;	tmk_core/protocol/ch555/usb_ak820.c:318: pD0_EP0_BUF[0] = keyboard_protocol;
      005E5F 90 0B 9D         [24] 2672 	mov	dptr,#_keyboard_protocol
      005E62 E0               [24] 2673 	movx	a,@dptr
      005E63 90 10 00         [24] 2674 	mov	dptr,#0x1000
      005E66 F0               [24] 2675 	movx	@dptr,a
                                   2676 ;	tmk_core/protocol/ch555/usb_ak820.c:319: D0_EP0T_L = 1;
      005E67 90 22 08         [24] 2677 	mov	dptr,#0x2208
      005E6A 74 01            [12] 2678 	mov	a,#0x01
      005E6C F0               [24] 2679 	movx	@dptr,a
                                   2680 ;	tmk_core/protocol/ch555/usb_ak820.c:320: control_phase = CTRL_STATUS_OUT;
      005E6D 90 06 E4         [24] 2681 	mov	dptr,#_control_phase
      005E70 04               [12] 2682 	inc	a
      005E71 F0               [24] 2683 	movx	@dptr,a
      005E72 02 5E F9         [24] 2684 	ljmp	00287$
      005E75                       2685 00207$:
                                   2686 ;	tmk_core/protocol/ch555/usb_ak820.c:321: } else if (index < TOTAL_INTERFACES && D0UsbConfig && type == 0x21 && D0SetupReqCode == DEF_USB_SET_IDLE && !D0SetupLen) {
      005E75 C3               [12] 2687 	clr	c
      005E76 EB               [12] 2688 	mov	a,r3
      005E77 94 03            [12] 2689 	subb	a,#0x03
      005E79 EC               [12] 2690 	mov	a,r4
      005E7A 94 00            [12] 2691 	subb	a,#0x00
      005E7C E4               [12] 2692 	clr	a
      005E7D 33               [12] 2693 	rlc	a
      005E7E F9               [12] 2694 	mov	r1,a
      005E7F 60 2C            [24] 2695 	jz	00200$
      005E81 90 06 8B         [24] 2696 	mov	dptr,#_D0UsbConfig
      005E84 E0               [24] 2697 	movx	a,@dptr
      005E85 60 26            [24] 2698 	jz	00200$
      005E87 EF               [12] 2699 	mov	a,r7
      005E88 60 23            [24] 2700 	jz	00200$
      005E8A 90 06 85         [24] 2701 	mov	dptr,#_D0SetupReqCode
      005E8D E0               [24] 2702 	movx	a,@dptr
      005E8E FF               [12] 2703 	mov	r7,a
      005E8F BF 0A 1B         [24] 2704 	cjne	r7,#0x0a,00200$
      005E92 90 06 86         [24] 2705 	mov	dptr,#_D0SetupLen
      005E95 E0               [24] 2706 	movx	a,@dptr
      005E96 F8               [12] 2707 	mov	r0,a
      005E97 A3               [24] 2708 	inc	dptr
      005E98 E0               [24] 2709 	movx	a,@dptr
      005E99 48               [12] 2710 	orl	a,r0
      005E9A 70 11            [24] 2711 	jnz	00200$
                                   2712 ;	tmk_core/protocol/ch555/usb_ak820.c:322: if (index == KEYBOARD_INTERFACE) keyboard_idle = value >> 8;
      005E9C EB               [12] 2713 	mov	a,r3
      005E9D 4C               [12] 2714 	orl	a,r4
      005E9E 70 05            [24] 2715 	jnz	00190$
      005EA0 90 05 5A         [24] 2716 	mov	dptr,#_keyboard_idle
      005EA3 EE               [12] 2717 	mov	a,r6
      005EA4 F0               [24] 2718 	movx	@dptr,a
      005EA5                       2719 00190$:
                                   2720 ;	tmk_core/protocol/ch555/usb_ak820.c:323: control_phase = CTRL_STATUS_IN;
      005EA5 90 06 E4         [24] 2721 	mov	dptr,#_control_phase
      005EA8 74 03            [12] 2722 	mov	a,#0x03
      005EAA F0               [24] 2723 	movx	@dptr,a
      005EAB 80 4C            [24] 2724 	sjmp	00287$
      005EAD                       2725 00200$:
                                   2726 ;	tmk_core/protocol/ch555/usb_ak820.c:324: } else if (index < TOTAL_INTERFACES && D0UsbConfig && type == 0xa1 && D0SetupReqCode == DEF_USB_GET_IDLE && !(value >> 8) && D0SetupLen == 1) {
      005EAD E9               [12] 2727 	mov	a,r1
      005EAE 60 46            [24] 2728 	jz	00192$
      005EB0 90 06 8B         [24] 2729 	mov	dptr,#_D0UsbConfig
      005EB3 E0               [24] 2730 	movx	a,@dptr
      005EB4 60 40            [24] 2731 	jz	00192$
      005EB6 EA               [12] 2732 	mov	a,r2
      005EB7 60 3D            [24] 2733 	jz	00192$
      005EB9 90 06 85         [24] 2734 	mov	dptr,#_D0SetupReqCode
      005EBC E0               [24] 2735 	movx	a,@dptr
      005EBD FF               [12] 2736 	mov	r7,a
      005EBE BF 02 35         [24] 2737 	cjne	r7,#0x02,00192$
      005EC1 8E 05            [24] 2738 	mov	ar5,r6
      005EC3 7E 00            [12] 2739 	mov	r6,#0x00
      005EC5 ED               [12] 2740 	mov	a,r5
      005EC6 4E               [12] 2741 	orl	a,r6
      005EC7 70 2D            [24] 2742 	jnz	00192$
      005EC9 90 06 86         [24] 2743 	mov	dptr,#_D0SetupLen
      005ECC E0               [24] 2744 	movx	a,@dptr
      005ECD FE               [12] 2745 	mov	r6,a
      005ECE A3               [24] 2746 	inc	dptr
      005ECF E0               [24] 2747 	movx	a,@dptr
      005ED0 FF               [12] 2748 	mov	r7,a
      005ED1 BE 01 22         [24] 2749 	cjne	r6,#0x01,00192$
      005ED4 BF 00 1F         [24] 2750 	cjne	r7,#0x00,00192$
                                   2751 ;	tmk_core/protocol/ch555/usb_ak820.c:325: pD0_EP0_BUF[0] = index == KEYBOARD_INTERFACE ? keyboard_idle : 0;
      005ED7 EB               [12] 2752 	mov	a,r3
      005ED8 4C               [12] 2753 	orl	a,r4
      005ED9 70 07            [24] 2754 	jnz	00324$
      005EDB 90 05 5A         [24] 2755 	mov	dptr,#_keyboard_idle
      005EDE E0               [24] 2756 	movx	a,@dptr
      005EDF FF               [12] 2757 	mov	r7,a
      005EE0 80 02            [24] 2758 	sjmp	00325$
      005EE2                       2759 00324$:
      005EE2 7F 00            [12] 2760 	mov	r7,#0x00
      005EE4                       2761 00325$:
      005EE4 90 10 00         [24] 2762 	mov	dptr,#0x1000
      005EE7 EF               [12] 2763 	mov	a,r7
      005EE8 F0               [24] 2764 	movx	@dptr,a
                                   2765 ;	tmk_core/protocol/ch555/usb_ak820.c:326: D0_EP0T_L = 1;
      005EE9 90 22 08         [24] 2766 	mov	dptr,#0x2208
      005EEC 74 01            [12] 2767 	mov	a,#0x01
      005EEE F0               [24] 2768 	movx	@dptr,a
                                   2769 ;	tmk_core/protocol/ch555/usb_ak820.c:327: control_phase = CTRL_STATUS_OUT;
      005EEF 90 06 E4         [24] 2770 	mov	dptr,#_control_phase
      005EF2 04               [12] 2771 	inc	a
      005EF3 F0               [24] 2772 	movx	@dptr,a
      005EF4 80 03            [24] 2773 	sjmp	00287$
      005EF6                       2774 00192$:
                                   2775 ;	tmk_core/protocol/ch555/usb_ak820.c:328: } else { control_stall(); return; }
      005EF6 02 54 8E         [24] 2776 	ljmp	_control_stall
      005EF9                       2777 00287$:
                                   2778 ;	tmk_core/protocol/ch555/usb_ak820.c:329: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
      005EF9 90 22 00         [24] 2779 	mov	dptr,#0x2200
      005EFC 74 C0            [12] 2780 	mov	a,#0xc0
      005EFE F0               [24] 2781 	movx	@dptr,a
                                   2782 ;	tmk_core/protocol/ch555/usb_ak820.c:330: }
      005EFF 22               [24] 2783 	ret
                                   2784 ;------------------------------------------------------------
                                   2785 ;Allocation info for local variables in function 'control_out'
                                   2786 ;------------------------------------------------------------
                                   2787 ;i             Allocated with name '_control_out_i_10000_360'
                                   2788 ;------------------------------------------------------------
                                   2789 ;	tmk_core/protocol/ch555/usb_ak820.c:332: static void control_out(void) {
                                   2790 ;	-----------------------------------------
                                   2791 ;	 function control_out
                                   2792 ;	-----------------------------------------
      005F00                       2793 _control_out:
                                   2794 ;	tmk_core/protocol/ch555/usb_ak820.c:334: if (!(D0_STATUS & bUXS_TOG_OK)) return; /* duplicate OUT is not a new request */
      005F00 90 22 0F         [24] 2795 	mov	dptr,#0x220f
      005F03 E0               [24] 2796 	movx	a,@dptr
      005F04 20 E6 01         [24] 2797 	jb	acc.6,00102$
      005F07 22               [24] 2798 	ret
      005F08                       2799 00102$:
                                   2800 ;	tmk_core/protocol/ch555/usb_ak820.c:335: if (control_phase == CTRL_STATUS_OUT && D0_RX_LEN == 0) {
      005F08 90 06 E4         [24] 2801 	mov	dptr,#_control_phase
      005F0B E0               [24] 2802 	movx	a,@dptr
      005F0C FF               [12] 2803 	mov	r7,a
      005F0D BF 02 12         [24] 2804 	cjne	r7,#0x02,00104$
      005F10 90 22 0E         [24] 2805 	mov	dptr,#0x220e
      005F13 E0               [24] 2806 	movx	a,@dptr
      005F14 70 0C            [24] 2807 	jnz	00104$
                                   2808 ;	tmk_core/protocol/ch555/usb_ak820.c:336: control_phase = CTRL_IDLE;
      005F16 90 06 E4         [24] 2809 	mov	dptr,#_control_phase
      005F19 E4               [12] 2810 	clr	a
      005F1A F0               [24] 2811 	movx	@dptr,a
                                   2812 ;	tmk_core/protocol/ch555/usb_ak820.c:337: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      005F1B 90 22 00         [24] 2813 	mov	dptr,#0x2200
      005F1E 74 02            [12] 2814 	mov	a,#0x02
      005F20 F0               [24] 2815 	movx	@dptr,a
                                   2816 ;	tmk_core/protocol/ch555/usb_ak820.c:338: return;
      005F21 22               [24] 2817 	ret
      005F22                       2818 00104$:
                                   2819 ;	tmk_core/protocol/ch555/usb_ak820.c:340: if (control_phase != CTRL_DATA_OUT || D0_RX_LEN != D0SetupLen) { control_stall(); return; }
      005F22 BF 04 19         [24] 2820 	cjne	r7,#0x04,00106$
      005F25 90 22 0E         [24] 2821 	mov	dptr,#0x220e
      005F28 E0               [24] 2822 	movx	a,@dptr
      005F29 FF               [12] 2823 	mov	r7,a
      005F2A 90 06 86         [24] 2824 	mov	dptr,#_D0SetupLen
      005F2D E0               [24] 2825 	movx	a,@dptr
      005F2E FD               [12] 2826 	mov	r5,a
      005F2F A3               [24] 2827 	inc	dptr
      005F30 E0               [24] 2828 	movx	a,@dptr
      005F31 FE               [12] 2829 	mov	r6,a
      005F32 7C 00            [12] 2830 	mov	r4,#0x00
      005F34 EF               [12] 2831 	mov	a,r7
      005F35 B5 05 06         [24] 2832 	cjne	a,ar5,00209$
      005F38 EC               [12] 2833 	mov	a,r4
      005F39 B5 06 02         [24] 2834 	cjne	a,ar6,00209$
      005F3C 80 03            [24] 2835 	sjmp	00107$
      005F3E                       2836 00209$:
      005F3E                       2837 00106$:
      005F3E 02 54 8E         [24] 2838 	ljmp	_control_stall
      005F41                       2839 00107$:
                                   2840 ;	tmk_core/protocol/ch555/usb_ak820.c:341: if (output_kind == OUTPUT_RAW && raw_state == RAW_RX) {
      005F41 90 06 E5         [24] 2841 	mov	dptr,#_output_kind
      005F44 E0               [24] 2842 	movx	a,@dptr
      005F45 FF               [12] 2843 	mov	r7,a
      005F46 BF 01 2E         [24] 2844 	cjne	r7,#0x01,00118$
      005F49 90 06 93         [24] 2845 	mov	dptr,#_raw_state
      005F4C E0               [24] 2846 	movx	a,@dptr
      005F4D FE               [12] 2847 	mov	r6,a
      005F4E BE 01 26         [24] 2848 	cjne	r6,#0x01,00118$
                                   2849 ;	tmk_core/protocol/ch555/usb_ak820.c:342: for (i = 0; i < RAW_EPSIZE; ++i) raw_buffer[i] = pD0_EP0_BUF[i];
      005F51 7E 00            [12] 2850 	mov	r6,#0x00
      005F53                       2851 00121$:
      005F53 EE               [12] 2852 	mov	a,r6
      005F54 24 94            [12] 2853 	add	a, #_raw_buffer
      005F56 FC               [12] 2854 	mov	r4,a
      005F57 E4               [12] 2855 	clr	a
      005F58 34 06            [12] 2856 	addc	a, #(_raw_buffer >> 8)
      005F5A FD               [12] 2857 	mov	r5,a
      005F5B 8E 82            [24] 2858 	mov	dpl,r6
      005F5D 74 10            [12] 2859 	mov	a,#0x10
      005F5F 24 00            [12] 2860 	add	a, #0x00
      005F61 F5 83            [12] 2861 	mov	dph,a
      005F63 E0               [24] 2862 	movx	a,@dptr
      005F64 8C 82            [24] 2863 	mov	dpl,r4
      005F66 8D 83            [24] 2864 	mov	dph,r5
      005F68 F0               [24] 2865 	movx	@dptr,a
      005F69 0E               [12] 2866 	inc	r6
      005F6A BE 20 00         [24] 2867 	cjne	r6,#0x20,00214$
      005F6D                       2868 00214$:
      005F6D 40 E4            [24] 2869 	jc	00121$
                                   2870 ;	tmk_core/protocol/ch555/usb_ak820.c:343: raw_state = RAW_READY; /* publish only after the entire packet is copied */
      005F6F 90 06 93         [24] 2871 	mov	dptr,#_raw_state
      005F72 74 02            [12] 2872 	mov	a,#0x02
      005F74 F0               [24] 2873 	movx	@dptr,a
      005F75 80 2B            [24] 2874 	sjmp	00119$
      005F77                       2875 00118$:
                                   2876 ;	tmk_core/protocol/ch555/usb_ak820.c:344: } else if (output_kind == OUTPUT_LED) {
      005F77 BF 02 0A         [24] 2877 	cjne	r7,#0x02,00115$
                                   2878 ;	tmk_core/protocol/ch555/usb_ak820.c:345: KB_USB_SetReport = pD0_EP0_BUF[0];
      005F7A 90 10 00         [24] 2879 	mov	dptr,#0x1000
      005F7D E0               [24] 2880 	movx	a,@dptr
      005F7E 90 06 90         [24] 2881 	mov	dptr,#_KB_USB_SetReport
      005F81 F0               [24] 2882 	movx	@dptr,a
      005F82 80 1E            [24] 2883 	sjmp	00119$
      005F84                       2884 00115$:
                                   2885 ;	tmk_core/protocol/ch555/usb_ak820.c:346: } else if (output_kind == OUTPUT_SHARED_LED && pD0_EP0_BUF[0] == output_report_id) {
      005F84 BF 03 18         [24] 2886 	cjne	r7,#0x03,00111$
      005F87 90 10 00         [24] 2887 	mov	dptr,#0x1000
      005F8A E0               [24] 2888 	movx	a,@dptr
      005F8B FF               [12] 2889 	mov	r7,a
      005F8C 90 06 E6         [24] 2890 	mov	dptr,#_output_report_id
      005F8F E0               [24] 2891 	movx	a,@dptr
      005F90 FE               [12] 2892 	mov	r6,a
      005F91 EF               [12] 2893 	mov	a,r7
      005F92 B5 06 0A         [24] 2894 	cjne	a,ar6,00111$
                                   2895 ;	tmk_core/protocol/ch555/usb_ak820.c:347: KB_USB_SetReport = pD0_EP0_BUF[1];
      005F95 90 10 01         [24] 2896 	mov	dptr,#0x1001
      005F98 E0               [24] 2897 	movx	a,@dptr
      005F99 90 06 90         [24] 2898 	mov	dptr,#_KB_USB_SetReport
      005F9C F0               [24] 2899 	movx	@dptr,a
      005F9D 80 03            [24] 2900 	sjmp	00119$
      005F9F                       2901 00111$:
                                   2902 ;	tmk_core/protocol/ch555/usb_ak820.c:348: } else { control_stall(); return; }
      005F9F 02 54 8E         [24] 2903 	ljmp	_control_stall
      005FA2                       2904 00119$:
                                   2905 ;	tmk_core/protocol/ch555/usb_ak820.c:349: output_kind = OUTPUT_NONE;
      005FA2 90 06 E5         [24] 2906 	mov	dptr,#_output_kind
      005FA5 E4               [12] 2907 	clr	a
      005FA6 F0               [24] 2908 	movx	@dptr,a
                                   2909 ;	tmk_core/protocol/ch555/usb_ak820.c:350: D0SetupLen = 0;
      005FA7 90 06 86         [24] 2910 	mov	dptr,#_D0SetupLen
      005FAA F0               [24] 2911 	movx	@dptr,a
      005FAB A3               [24] 2912 	inc	dptr
      005FAC F0               [24] 2913 	movx	@dptr,a
                                   2914 ;	tmk_core/protocol/ch555/usb_ak820.c:351: control_phase = CTRL_STATUS_IN;
      005FAD 90 06 E4         [24] 2915 	mov	dptr,#_control_phase
      005FB0 74 03            [12] 2916 	mov	a,#0x03
      005FB2 F0               [24] 2917 	movx	@dptr,a
                                   2918 ;	tmk_core/protocol/ch555/usb_ak820.c:352: D0_EP0T_L = 0;
      005FB3 90 22 08         [24] 2919 	mov	dptr,#0x2208
      005FB6 E4               [12] 2920 	clr	a
      005FB7 F0               [24] 2921 	movx	@dptr,a
                                   2922 ;	tmk_core/protocol/ch555/usb_ak820.c:353: D0_EP0RES = bUEP_T_TOG | UEP_R_RES_NAK | UEP_T_RES_ACK;
      005FB8 F5 82            [12] 2923 	mov	dpl,a
      005FBA 74 48            [12] 2924 	mov	a,#0x48
      005FBC F0               [24] 2925 	movx	@dptr,a
                                   2926 ;	tmk_core/protocol/ch555/usb_ak820.c:354: }
      005FBD 22               [24] 2927 	ret
                                   2928 ;------------------------------------------------------------
                                   2929 ;Allocation info for local variables in function 'control_in'
                                   2930 ;------------------------------------------------------------
                                   2931 ;	tmk_core/protocol/ch555/usb_ak820.c:356: static void control_in(void) {
                                   2932 ;	-----------------------------------------
                                   2933 ;	 function control_in
                                   2934 ;	-----------------------------------------
      005FBE                       2935 _control_in:
                                   2936 ;	tmk_core/protocol/ch555/usb_ak820.c:357: if (control_phase == CTRL_DATA_IN) {
      005FBE 90 06 E4         [24] 2937 	mov	dptr,#_control_phase
      005FC1 E0               [24] 2938 	movx	a,@dptr
      005FC2 FF               [12] 2939 	mov	r7,a
      005FC3 BF 01 22         [24] 2940 	cjne	r7,#0x01,00109$
                                   2941 ;	tmk_core/protocol/ch555/usb_ak820.c:358: if (D0SetupLen || control_zlp) {
      005FC6 90 06 86         [24] 2942 	mov	dptr,#_D0SetupLen
      005FC9 E0               [24] 2943 	movx	a,@dptr
      005FCA FD               [12] 2944 	mov	r5,a
      005FCB A3               [24] 2945 	inc	dptr
      005FCC E0               [24] 2946 	movx	a,@dptr
      005FCD 4D               [12] 2947 	orl	a,r5
      005FCE 70 06            [24] 2948 	jnz	00101$
      005FD0 90 06 E7         [24] 2949 	mov	dptr,#_control_zlp
      005FD3 E0               [24] 2950 	movx	a,@dptr
      005FD4 60 0A            [24] 2951 	jz	00102$
      005FD6                       2952 00101$:
                                   2953 ;	tmk_core/protocol/ch555/usb_ak820.c:359: D0_EP0RES ^= bUEP_T_TOG;
      005FD6 90 22 00         [24] 2954 	mov	dptr,#0x2200
      005FD9 E0               [24] 2955 	movx	a,@dptr
      005FDA 64 40            [12] 2956 	xrl	a,#0x40
      005FDC F0               [24] 2957 	movx	@dptr,a
                                   2958 ;	tmk_core/protocol/ch555/usb_ak820.c:360: control_next();
                                   2959 ;	tmk_core/protocol/ch555/usb_ak820.c:361: return;
      005FDD 02 54 B0         [24] 2960 	ljmp	_control_next
      005FE0                       2961 00102$:
                                   2962 ;	tmk_core/protocol/ch555/usb_ak820.c:363: control_phase = CTRL_STATUS_OUT;
      005FE0 90 06 E4         [24] 2963 	mov	dptr,#_control_phase
      005FE3 74 02            [12] 2964 	mov	a,#0x02
      005FE5 F0               [24] 2965 	movx	@dptr,a
      005FE6 80 18            [24] 2966 	sjmp	00110$
      005FE8                       2967 00109$:
                                   2968 ;	tmk_core/protocol/ch555/usb_ak820.c:364: } else if (control_phase == CTRL_STATUS_IN) {
      005FE8 BF 03 15         [24] 2969 	cjne	r7,#0x03,00110$
                                   2970 ;	tmk_core/protocol/ch555/usb_ak820.c:365: if (D0SetupReqCode == USB_SET_ADDRESS) D0_ADDR = D0SetupLen;
      005FEB 90 06 85         [24] 2971 	mov	dptr,#_D0SetupReqCode
      005FEE E0               [24] 2972 	movx	a,@dptr
      005FEF FF               [12] 2973 	mov	r7,a
      005FF0 BF 05 08         [24] 2974 	cjne	r7,#0x05,00105$
      005FF3 90 06 86         [24] 2975 	mov	dptr,#_D0SetupLen
      005FF6 E0               [24] 2976 	movx	a,@dptr
      005FF7 90 22 07         [24] 2977 	mov	dptr,#0x2207
      005FFA F0               [24] 2978 	movx	@dptr,a
      005FFB                       2979 00105$:
                                   2980 ;	tmk_core/protocol/ch555/usb_ak820.c:366: control_phase = CTRL_IDLE;
      005FFB 90 06 E4         [24] 2981 	mov	dptr,#_control_phase
      005FFE E4               [12] 2982 	clr	a
      005FFF F0               [24] 2983 	movx	@dptr,a
      006000                       2984 00110$:
                                   2985 ;	tmk_core/protocol/ch555/usb_ak820.c:368: D0_EP0RES = bUEP_R_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
      006000 90 22 00         [24] 2986 	mov	dptr,#0x2200
      006003 74 82            [12] 2987 	mov	a,#0x82
      006005 F0               [24] 2988 	movx	@dptr,a
                                   2989 ;	tmk_core/protocol/ch555/usb_ak820.c:369: }
      006006 22               [24] 2990 	ret
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
      006007                       3001 _USB_DeviceInterrupt:
                                   3002 ;	tmk_core/protocol/ch555/usb_ak820.c:374: do {
      006007                       3003 00129$:
                                   3004 ;	tmk_core/protocol/ch555/usb_ak820.c:376: if (USB_IF & bUX_IF_BUS_RST) {
      006007 90 22 3D         [24] 3005 	mov	dptr,#0x223d
      00600A E0               [24] 3006 	movx	a,@dptr
      00600B 30 E0 4B         [24] 3007 	jnb	acc.0,00127$
                                   3008 ;	tmk_core/protocol/ch555/usb_ak820.c:377: endpoints_reset();
      00600E 12 54 37         [24] 3009 	lcall	_endpoints_reset
                                   3010 ;	tmk_core/protocol/ch555/usb_ak820.c:378: D0_ADDR = 0;
      006011 90 22 07         [24] 3011 	mov	dptr,#0x2207
      006014 E4               [12] 3012 	clr	a
      006015 F0               [24] 3013 	movx	@dptr,a
                                   3014 ;	tmk_core/protocol/ch555/usb_ak820.c:379: D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
      006016 90 06 8D         [24] 3015 	mov	dptr,#_USB_SleepStatus
      006019 F0               [24] 3016 	movx	@dptr,a
      00601A 90 06 8C         [24] 3017 	mov	dptr,#_USB_EnumStatus
      00601D F0               [24] 3018 	movx	@dptr,a
      00601E 90 06 8B         [24] 3019 	mov	dptr,#_D0UsbConfig
      006021 F0               [24] 3020 	movx	@dptr,a
                                   3021 ;	tmk_core/protocol/ch555/usb_ak820.c:380: KB_USB_SetReport = 0;
      006022 90 06 90         [24] 3022 	mov	dptr,#_KB_USB_SetReport
      006025 F0               [24] 3023 	movx	@dptr,a
                                   3024 ;	tmk_core/protocol/ch555/usb_ak820.c:381: keyboard_protocol = 1;
      006026 90 0B 9D         [24] 3025 	mov	dptr,#_keyboard_protocol
      006029 04               [12] 3026 	inc	a
      00602A F0               [24] 3027 	movx	@dptr,a
                                   3028 ;	tmk_core/protocol/ch555/usb_ak820.c:382: keyboard_idle = 0;
      00602B 90 05 5A         [24] 3029 	mov	dptr,#_keyboard_idle
      00602E E4               [12] 3030 	clr	a
      00602F F0               [24] 3031 	movx	@dptr,a
                                   3032 ;	tmk_core/protocol/ch555/usb_ak820.c:383: keyboard_reset = 1;
      006030 90 06 B5         [24] 3033 	mov	dptr,#_keyboard_reset
      006033 04               [12] 3034 	inc	a
      006034 F0               [24] 3035 	movx	@dptr,a
                                   3036 ;	tmk_core/protocol/ch555/usb_ak820.c:384: D0SetupReqCode = 0xff;
      006035 90 06 85         [24] 3037 	mov	dptr,#_D0SetupReqCode
      006038 74 FF            [12] 3038 	mov	a,#0xff
      00603A F0               [24] 3039 	movx	@dptr,a
                                   3040 ;	tmk_core/protocol/ch555/usb_ak820.c:385: D0SetupLen = 0;
      00603B 90 06 86         [24] 3041 	mov	dptr,#_D0SetupLen
      00603E E4               [12] 3042 	clr	a
      00603F F0               [24] 3043 	movx	@dptr,a
      006040 A3               [24] 3044 	inc	dptr
      006041 F0               [24] 3045 	movx	@dptr,a
                                   3046 ;	tmk_core/protocol/ch555/usb_ak820.c:386: control_phase = CTRL_IDLE;
      006042 90 06 E4         [24] 3047 	mov	dptr,#_control_phase
      006045 F0               [24] 3048 	movx	@dptr,a
                                   3049 ;	tmk_core/protocol/ch555/usb_ak820.c:387: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      006046 90 22 00         [24] 3050 	mov	dptr,#0x2200
      006049 74 02            [12] 3051 	mov	a,#0x02
      00604B F0               [24] 3052 	movx	@dptr,a
                                   3053 ;	tmk_core/protocol/ch555/usb_ak820.c:388: ACK_TRANSFER();
      00604C 90 22 0F         [24] 3054 	mov	dptr,#0x220f
      00604F E4               [12] 3055 	clr	a
      006050 F0               [24] 3056 	movx	@dptr,a
                                   3057 ;	tmk_core/protocol/ch555/usb_ak820.c:389: ACK_RESET();
      006051 90 22 3D         [24] 3058 	mov	dptr,#0x223d
      006054 04               [12] 3059 	inc	a
      006055 F0               [24] 3060 	movx	@dptr,a
      006056 02 60 EC         [24] 3061 	ljmp	00130$
      006059                       3062 00127$:
                                   3063 ;	tmk_core/protocol/ch555/usb_ak820.c:390: } else if (USB_IF & bUX_IF_D0_TRANS) {
      006059 90 22 3D         [24] 3064 	mov	dptr,#0x223d
      00605C E0               [24] 3065 	movx	a,@dptr
      00605D 30 E5 60         [24] 3066 	jnb	acc.5,00124$
                                   3067 ;	tmk_core/protocol/ch555/usb_ak820.c:391: status = D0_STATUS;
      006060 90 22 0F         [24] 3068 	mov	dptr,#0x220f
      006063 E0               [24] 3069 	movx	a,@dptr
      006064 FF               [12] 3070 	mov	r7,a
                                   3071 ;	tmk_core/protocol/ch555/usb_ak820.c:392: endpoint = status & MASK_UXS_ENDP;
      006065 74 07            [12] 3072 	mov	a,#0x07
      006067 5F               [12] 3073 	anl	a,r7
      006068 FE               [12] 3074 	mov	r6,a
                                   3075 ;	tmk_core/protocol/ch555/usb_ak820.c:396: if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_OUT && !endpoint) {
      006069 EF               [12] 3076 	mov	a,r7
      00606A 54 18            [12] 3077 	anl	a,#0x18
      00606C 70 08            [24] 3078 	jnz	00115$
      00606E EE               [12] 3079 	mov	a,r6
      00606F 70 05            [24] 3080 	jnz	00115$
                                   3081 ;	tmk_core/protocol/ch555/usb_ak820.c:397: control_out();
      006071 12 5F 00         [24] 3082 	lcall	_control_out
      006074 80 43            [24] 3083 	sjmp	00116$
      006076                       3084 00115$:
                                   3085 ;	tmk_core/protocol/ch555/usb_ak820.c:398: } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_IN) {
      006076 8F 05            [24] 3086 	mov	ar5,r7
      006078 74 18            [12] 3087 	mov	a,#0x18
      00607A 5D               [12] 3088 	anl	a,r5
      00607B FC               [12] 3089 	mov	r4,a
      00607C BC 10 2D         [24] 3090 	cjne	r4,#0x10,00112$
                                   3091 ;	tmk_core/protocol/ch555/usb_ak820.c:399: if (!endpoint) control_in();
      00607F EE               [12] 3092 	mov	a,r6
      006080 70 05            [24] 3093 	jnz	00106$
      006082 12 5F BE         [24] 3094 	lcall	_control_in
      006085 80 32            [24] 3095 	sjmp	00116$
      006087                       3096 00106$:
                                   3097 ;	tmk_core/protocol/ch555/usb_ak820.c:400: else if (endpoint <= 3) {
      006087 EE               [12] 3098 	mov	a,r6
      006088 24 FC            [12] 3099 	add	a,#0xff - 0x03
      00608A 40 2D            [24] 3100 	jc	00116$
                                   3101 ;	free result
                                   3102 ;	tmk_core/protocol/ch555/usb_ak820.c:401: EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_NAK;
      00608C 8E 04            [24] 3103 	mov	ar4,r6
      00608E 7B 00            [12] 3104 	mov	r3,#0x00
      006090 74 22            [12] 3105 	mov	a,#0x22
      006092 2B               [12] 3106 	add	a, r3
      006093 FB               [12] 3107 	mov	r3,a
      006094 8C 82            [24] 3108 	mov	dpl,r4
      006096 8B 83            [24] 3109 	mov	dph,r3
      006098 E0               [24] 3110 	movx	a,@dptr
      006099 FA               [12] 3111 	mov	r2,a
      00609A 74 FC            [12] 3112 	mov	a,#0xfc
      00609C 5A               [12] 3113 	anl	a,r2
      00609D 44 02            [12] 3114 	orl	a,#0x02
      00609F 8C 82            [24] 3115 	mov	dpl,r4
      0060A1 8B 83            [24] 3116 	mov	dph,r3
      0060A3 F0               [24] 3117 	movx	@dptr,a
                                   3118 ;	tmk_core/protocol/ch555/usb_ak820.c:402: if (endpoint == RAW_IN_EPNUM) raw_complete();
      0060A4 BE 03 12         [24] 3119 	cjne	r6,#0x03,00116$
      0060A7 12 54 1A         [24] 3120 	lcall	_raw_complete
      0060AA 80 0D            [24] 3121 	sjmp	00116$
      0060AC                       3122 00112$:
                                   3123 ;	tmk_core/protocol/ch555/usb_ak820.c:404: } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_FREE && (status & bUXS_SETUP_ACT)) {
      0060AC 53 05 18         [24] 3124 	anl	ar5,#0x18
      0060AF BD 18 07         [24] 3125 	cjne	r5,#0x18,00116$
      0060B2 EF               [12] 3126 	mov	a,r7
      0060B3 30 E5 03         [24] 3127 	jnb	acc.5,00116$
                                   3128 ;	tmk_core/protocol/ch555/usb_ak820.c:405: control_setup();
      0060B6 12 56 F5         [24] 3129 	lcall	_control_setup
      0060B9                       3130 00116$:
                                   3131 ;	tmk_core/protocol/ch555/usb_ak820.c:407: ACK_TRANSFER();
      0060B9 90 22 0F         [24] 3132 	mov	dptr,#0x220f
      0060BC E4               [12] 3133 	clr	a
      0060BD F0               [24] 3134 	movx	@dptr,a
      0060BE 80 2C            [24] 3135 	sjmp	00130$
      0060C0                       3136 00124$:
                                   3137 ;	tmk_core/protocol/ch555/usb_ak820.c:408: } else if (USB_IF & bUX_IF_SUSPEND) {
      0060C0 90 22 3D         [24] 3138 	mov	dptr,#0x223d
      0060C3 E0               [24] 3139 	movx	a,@dptr
      0060C4 30 E2 25         [24] 3140 	jnb	acc.2,00130$
                                   3141 ;	tmk_core/protocol/ch555/usb_ak820.c:409: if (USB_IF & bUX_SUSPEND) USB_SleepStatus |= 2;
      0060C7 90 22 3D         [24] 3142 	mov	dptr,#0x223d
      0060CA E0               [24] 3143 	movx	a,@dptr
      0060CB 30 E3 0A         [24] 3144 	jnb	acc.3,00119$
      0060CE 90 06 8D         [24] 3145 	mov	dptr,#_USB_SleepStatus
      0060D1 E0               [24] 3146 	movx	a,@dptr
      0060D2 43 E0 02         [24] 3147 	orl	acc,#0x02
      0060D5 F0               [24] 3148 	movx	@dptr,a
      0060D6 80 0E            [24] 3149 	sjmp	00120$
      0060D8                       3150 00119$:
                                   3151 ;	tmk_core/protocol/ch555/usb_ak820.c:411: USB_SleepStatus &= ~2;
      0060D8 90 06 8D         [24] 3152 	mov	dptr,#_USB_SleepStatus
      0060DB E0               [24] 3153 	movx	a,@dptr
      0060DC 53 E0 FD         [24] 3154 	anl	acc,#0xfd
      0060DF F0               [24] 3155 	movx	@dptr,a
                                   3156 ;	tmk_core/protocol/ch555/usb_ak820.c:412: keyboard_reset = 1;
      0060E0 90 06 B5         [24] 3157 	mov	dptr,#_keyboard_reset
      0060E3 74 01            [12] 3158 	mov	a,#0x01
      0060E5 F0               [24] 3159 	movx	@dptr,a
      0060E6                       3160 00120$:
                                   3161 ;	tmk_core/protocol/ch555/usb_ak820.c:414: ACK_SUSPEND();
      0060E6 90 22 3D         [24] 3162 	mov	dptr,#0x223d
      0060E9 74 04            [12] 3163 	mov	a,#0x04
      0060EB F0               [24] 3164 	movx	@dptr,a
      0060EC                       3165 00130$:
                                   3166 ;	tmk_core/protocol/ch555/usb_ak820.c:416: } while (USB_IF & (bUX_IF_BUS_RST | bUX_IF_D0_TRANS | bUX_IF_SUSPEND));
      0060EC 90 22 3D         [24] 3167 	mov	dptr,#0x223d
      0060EF E0               [24] 3168 	movx	a,@dptr
      0060F0 54 25            [12] 3169 	anl	a,#0x25
      0060F2 60 03            [24] 3170 	jz	00242$
      0060F4 02 60 07         [24] 3171 	ljmp	00129$
      0060F7                       3172 00242$:
                                   3173 ;	tmk_core/protocol/ch555/usb_ak820.c:417: }
      0060F7 22               [24] 3174 	ret
                                   3175 ;------------------------------------------------------------
                                   3176 ;Allocation info for local variables in function 'USB_Device_Init'
                                   3177 ;------------------------------------------------------------
                                   3178 ;	tmk_core/protocol/ch555/usb_ak820.c:420: void USB_Device_Init(void) {
                                   3179 ;	-----------------------------------------
                                   3180 ;	 function USB_Device_Init
                                   3181 ;	-----------------------------------------
      0060F8                       3182 _USB_Device_Init:
                                   3183 ;	tmk_core/protocol/ch555/usb_ak820.c:421: IE_USB = 0;
                                   3184 ;	assignBit
      0060F8 C2 E9            [12] 3185 	clr	_IE_USB
                                   3186 ;	tmk_core/protocol/ch555/usb_ak820.c:422: USB_CTRL = 0;
      0060FA 90 22 3C         [24] 3187 	mov	dptr,#0x223c
      0060FD E4               [12] 3188 	clr	a
      0060FE F0               [24] 3189 	movx	@dptr,a
                                   3190 ;	tmk_core/protocol/ch555/usb_ak820.c:423: raw_state = RAW_IDLE;
      0060FF 90 06 93         [24] 3191 	mov	dptr,#_raw_state
      006102 F0               [24] 3192 	movx	@dptr,a
                                   3193 ;	tmk_core/protocol/ch555/usb_ak820.c:424: endpoints_reset();
      006103 12 54 37         [24] 3194 	lcall	_endpoints_reset
                                   3195 ;	tmk_core/protocol/ch555/usb_ak820.c:425: D0_ADDR = D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
      006106 90 06 8D         [24] 3196 	mov	dptr,#_USB_SleepStatus
      006109 E4               [12] 3197 	clr	a
      00610A F0               [24] 3198 	movx	@dptr,a
      00610B 90 06 8C         [24] 3199 	mov	dptr,#_USB_EnumStatus
      00610E F0               [24] 3200 	movx	@dptr,a
      00610F 90 06 8B         [24] 3201 	mov	dptr,#_D0UsbConfig
      006112 F0               [24] 3202 	movx	@dptr,a
      006113 90 22 07         [24] 3203 	mov	dptr,#0x2207
      006116 F0               [24] 3204 	movx	@dptr,a
                                   3205 ;	tmk_core/protocol/ch555/usb_ak820.c:426: KB_USB_SetReport = KB_USB_UpStatus = MCU_Sleep_Operate = 0;
      006117 90 06 8E         [24] 3206 	mov	dptr,#_MCU_Sleep_Operate
      00611A F0               [24] 3207 	movx	@dptr,a
      00611B 90 06 8F         [24] 3208 	mov	dptr,#_KB_USB_UpStatus
      00611E F0               [24] 3209 	movx	@dptr,a
      00611F 90 06 90         [24] 3210 	mov	dptr,#_KB_USB_SetReport
      006122 F0               [24] 3211 	movx	@dptr,a
                                   3212 ;	tmk_core/protocol/ch555/usb_ak820.c:427: keyboard_protocol = 1;
      006123 90 0B 9D         [24] 3213 	mov	dptr,#_keyboard_protocol
      006126 04               [12] 3214 	inc	a
      006127 F0               [24] 3215 	movx	@dptr,a
                                   3216 ;	tmk_core/protocol/ch555/usb_ak820.c:428: keyboard_idle = 0;
      006128 90 05 5A         [24] 3217 	mov	dptr,#_keyboard_idle
      00612B E4               [12] 3218 	clr	a
      00612C F0               [24] 3219 	movx	@dptr,a
                                   3220 ;	tmk_core/protocol/ch555/usb_ak820.c:429: keyboard_reset = 0;
      00612D 90 06 B5         [24] 3221 	mov	dptr,#_keyboard_reset
      006130 F0               [24] 3222 	movx	@dptr,a
                                   3223 ;	tmk_core/protocol/ch555/usb_ak820.c:430: control_phase = CTRL_IDLE;
      006131 90 06 E4         [24] 3224 	mov	dptr,#_control_phase
      006134 F0               [24] 3225 	movx	@dptr,a
                                   3226 ;	tmk_core/protocol/ch555/usb_ak820.c:431: D0SetupReqCode = 0xff;
      006135 90 06 85         [24] 3227 	mov	dptr,#_D0SetupReqCode
      006138 14               [12] 3228 	dec	a
      006139 F0               [24] 3229 	movx	@dptr,a
                                   3230 ;	tmk_core/protocol/ch555/usb_ak820.c:432: D0SetupLen = 0;
      00613A 90 06 86         [24] 3231 	mov	dptr,#_D0SetupLen
      00613D E4               [12] 3232 	clr	a
      00613E F0               [24] 3233 	movx	@dptr,a
      00613F A3               [24] 3234 	inc	dptr
      006140 F0               [24] 3235 	movx	@dptr,a
                                   3236 ;	tmk_core/protocol/ch555/usb_ak820.c:433: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      006141 90 22 00         [24] 3237 	mov	dptr,#0x2200
      006144 74 02            [12] 3238 	mov	a,#0x02
      006146 F0               [24] 3239 	movx	@dptr,a
                                   3240 ;	tmk_core/protocol/ch555/usb_ak820.c:434: HB_ADDR = 0x7f;
      006147 90 22 37         [24] 3241 	mov	dptr,#0x2237
      00614A 74 7F            [12] 3242 	mov	a,#0x7f
      00614C F0               [24] 3243 	movx	@dptr,a
                                   3244 ;	tmk_core/protocol/ch555/usb_ak820.c:435: ACK_ALL();
      00614D 90 22 3D         [24] 3245 	mov	dptr,#0x223d
      006150 74 FF            [12] 3246 	mov	a,#0xff
      006152 F0               [24] 3247 	movx	@dptr,a
                                   3248 ;	tmk_core/protocol/ch555/usb_ak820.c:436: USB_IE = bUX_IE_SUSPEND | bUX_IE_TRANSFER | bUX_IE_BUS_RST;
      006153 90 22 3B         [24] 3249 	mov	dptr,#0x223b
      006156 74 07            [12] 3250 	mov	a,#0x07
      006158 F0               [24] 3251 	movx	@dptr,a
                                   3252 ;	tmk_core/protocol/ch555/usb_ak820.c:437: USB_CTRL = bUX_DP_PU_EN;
      006159 A3               [24] 3253 	inc	dptr
      00615A 74 80            [12] 3254 	mov	a,#0x80
      00615C F0               [24] 3255 	movx	@dptr,a
                                   3256 ;	tmk_core/protocol/ch555/usb_ak820.c:438: IE_USB = 1;
                                   3257 ;	assignBit
      00615D D2 E9            [12] 3258 	setb	_IE_USB
                                   3259 ;	tmk_core/protocol/ch555/usb_ak820.c:439: }
      00615F 22               [24] 3260 	ret
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
      006160                       3271 _USB_WakeUp_PC:
                                   3272 ;	tmk_core/protocol/ch555/usb_ak820.c:443: if (USB_SleepStatus != 3) return;
      006160 90 06 8D         [24] 3273 	mov	dptr,#_USB_SleepStatus
      006163 E0               [24] 3274 	movx	a,@dptr
      006164 FF               [12] 3275 	mov	r7,a
      006165 BF 03 22         [24] 3276 	cjne	r7,#0x03,00110$
                                   3277 ;	tmk_core/protocol/ch555/usb_ak820.c:444: saved = USB_CTRL;
      006168 90 22 3C         [24] 3278 	mov	dptr,#0x223c
      00616B E0               [24] 3279 	movx	a,@dptr
      00616C FF               [12] 3280 	mov	r7,a
                                   3281 ;	tmk_core/protocol/ch555/usb_ak820.c:445: USB_CTRL ^= bUX_DP_PU_EN | bUX_DM_PU_EN;
      00616D E0               [24] 3282 	movx	a,@dptr
      00616E FE               [12] 3283 	mov	r6,a
      00616F 63 06 C0         [24] 3284 	xrl	ar6,#0xc0
      006172 90 22 3C         [24] 3285 	mov	dptr,#0x223c
      006175 EE               [12] 3286 	mov	a,r6
      006176 F0               [24] 3287 	movx	@dptr,a
                                   3288 ;	tmk_core/protocol/ch555/usb_ak820.c:446: wait_ms(10);
      006177 7E 0A            [12] 3289 	mov	r6,#0x0a
      006179                       3290 00108$:
      006179 EE               [12] 3291 	mov	a,r6
      00617A 60 09            [24] 3292 	jz	00105$
      00617C 90 00 01         [24] 3293 	mov	dptr,#0x0001
      00617F 12 52 5E         [24] 3294 	lcall	_mDelaymS
      006182 1E               [12] 3295 	dec	r6
      006183 80 F4            [24] 3296 	sjmp	00108$
      006185                       3297 00105$:
                                   3298 ;	tmk_core/protocol/ch555/usb_ak820.c:447: USB_CTRL = saved;
      006185 90 22 3C         [24] 3299 	mov	dptr,#0x223c
      006188 EF               [12] 3300 	mov	a,r7
      006189 F0               [24] 3301 	movx	@dptr,a
      00618A                       3302 00110$:
                                   3303 ;	tmk_core/protocol/ch555/usb_ak820.c:448: }
      00618A 22               [24] 3304 	ret
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
      00618B                       3325 _ak820_usb_send:
      00618B E5 82            [12] 3326 	mov	a,dpl
      00618D 90 06 F4         [24] 3327 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      006190 F0               [24] 3328 	movx	@dptr,a
                                   3329 ;	tmk_core/protocol/ch555/usb_ak820.c:454: uint8_t offset = SNAPSHOT_SIZE;
      006191 90 06 F5         [24] 3330 	mov	dptr,#_ak820_usb_send_offset_10000_413
      006194 74 2E            [12] 3331 	mov	a,#0x2e
      006196 F0               [24] 3332 	movx	@dptr,a
                                   3333 ;	tmk_core/protocol/ch555/usb_ak820.c:456: if (endpoint < 1 || endpoint > 3 || length > 64 || !USB_EnumStatus) return false;
      006197 90 06 F4         [24] 3334 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      00619A E0               [24] 3335 	movx	a,@dptr
      00619B FF               [12] 3336 	mov	r7,a
      00619C BF 01 00         [24] 3337 	cjne	r7,#0x01,00306$
      00619F                       3338 00306$:
      00619F 40 14            [24] 3339 	jc	00101$
      0061A1 EF               [12] 3340 	mov	a,r7
      0061A2 24 FC            [12] 3341 	add	a,#0xff - 0x03
      0061A4 40 0F            [24] 3342 	jc	00101$
                                   3343 ;	free result
      0061A6 90 06 F3         [24] 3344 	mov	dptr,#_ak820_usb_send_PARM_3
      0061A9 E0               [24] 3345 	movx	a,@dptr
      0061AA FE               [12] 3346 	mov  r6,a
      0061AB 24 BF            [12] 3347 	add	a,#0xff - 0x40
      0061AD 40 06            [24] 3348 	jc	00101$
                                   3349 ;	free result
      0061AF 90 06 8C         [24] 3350 	mov	dptr,#_USB_EnumStatus
      0061B2 E0               [24] 3351 	movx	a,@dptr
      0061B3 70 04            [24] 3352 	jnz	00102$
      0061B5                       3353 00101$:
      0061B5 75 82 00         [24] 3354 	mov	dpl, #0x00
      0061B8 22               [24] 3355 	ret
      0061B9                       3356 00102$:
                                   3357 ;	tmk_core/protocol/ch555/usb_ak820.c:457: if (endpoint == KEYBOARD_IN_EPNUM) {
      0061B9 BF 01 10         [24] 3358 	cjne	r7,#0x01,00118$
                                   3359 ;	tmk_core/protocol/ch555/usb_ak820.c:458: if (length != KEYBOARD_EPSIZE) return false;
      0061BC BE 08 02         [24] 3360 	cjne	r6,#0x08,00313$
      0061BF 80 04            [24] 3361 	sjmp	00107$
      0061C1                       3362 00313$:
      0061C1 75 82 00         [24] 3363 	mov	dpl, #0x00
      0061C4 22               [24] 3364 	ret
      0061C5                       3365 00107$:
                                   3366 ;	tmk_core/protocol/ch555/usb_ak820.c:459: offset = SNAPSHOT_KEYBOARD;
      0061C5 90 06 F5         [24] 3367 	mov	dptr,#_ak820_usb_send_offset_10000_413
      0061C8 E4               [12] 3368 	clr	a
      0061C9 F0               [24] 3369 	movx	@dptr,a
      0061CA 80 3C            [24] 3370 	sjmp	00119$
      0061CC                       3371 00118$:
                                   3372 ;	tmk_core/protocol/ch555/usb_ak820.c:460: } else if (endpoint == SHARED_IN_EPNUM) {
      0061CC BF 02 30         [24] 3373 	cjne	r7,#0x02,00115$
                                   3374 ;	tmk_core/protocol/ch555/usb_ak820.c:461: report_id = report[0];
      0061CF 90 06 F1         [24] 3375 	mov	dptr,#_ak820_usb_send_PARM_2
      0061D2 E0               [24] 3376 	movx	a,@dptr
      0061D3 FD               [12] 3377 	mov	r5,a
      0061D4 A3               [24] 3378 	inc	dptr
      0061D5 E0               [24] 3379 	movx	a,@dptr
      0061D6 FF               [12] 3380 	mov	r7,a
      0061D7 8D 82            [24] 3381 	mov	dpl,r5
      0061D9 8F 83            [24] 3382 	mov	dph,r7
      0061DB E0               [24] 3383 	movx	a,@dptr
      0061DC FF               [12] 3384 	mov	r7,a
                                   3385 ;	tmk_core/protocol/ch555/usb_ak820.c:462: if (report_id >= sizeof(shared_lengths) || !shared_lengths[report_id] || length != shared_lengths[report_id]) return false;
      0061DD BF 07 00         [24] 3386 	cjne	r7,#0x07,00316$
      0061E0                       3387 00316$:
      0061E0 50 0E            [24] 3388 	jnc	00108$
      0061E2 EF               [12] 3389 	mov	a,r7
      0061E3 90 B6 19         [24] 3390 	mov	dptr,#_shared_lengths
      0061E6 93               [24] 3391 	movc	a,@a+dptr
      0061E7 FD               [12] 3392 	mov	r5,a
      0061E8 60 06            [24] 3393 	jz	00108$
      0061EA EE               [12] 3394 	mov	a,r6
      0061EB B5 05 02         [24] 3395 	cjne	a,ar5,00319$
      0061EE 80 04            [24] 3396 	sjmp	00109$
      0061F0                       3397 00319$:
      0061F0                       3398 00108$:
      0061F0 75 82 00         [24] 3399 	mov	dpl, #0x00
      0061F3 22               [24] 3400 	ret
      0061F4                       3401 00109$:
                                   3402 ;	tmk_core/protocol/ch555/usb_ak820.c:463: offset = shared_offsets[report_id];
      0061F4 EF               [12] 3403 	mov	a,r7
      0061F5 90 B6 12         [24] 3404 	mov	dptr,#_shared_offsets
      0061F8 93               [24] 3405 	movc	a,@a+dptr
      0061F9 90 06 F5         [24] 3406 	mov	dptr,#_ak820_usb_send_offset_10000_413
      0061FC F0               [24] 3407 	movx	@dptr,a
      0061FD 80 09            [24] 3408 	sjmp	00119$
      0061FF                       3409 00115$:
                                   3410 ;	tmk_core/protocol/ch555/usb_ak820.c:464: } else if (length != RAW_EPSIZE) return false;
      0061FF BE 20 02         [24] 3411 	cjne	r6,#0x20,00320$
      006202 80 04            [24] 3412 	sjmp	00119$
      006204                       3413 00320$:
      006204 75 82 00         [24] 3414 	mov	dpl, #0x00
      006207 22               [24] 3415 	ret
      006208                       3416 00119$:
                                   3417 ;	tmk_core/protocol/ch555/usb_ak820.c:465: if (USB_SleepStatus & 2) { USB_WakeUp_PC(); return false; }
      006208 90 06 8D         [24] 3418 	mov	dptr,#_USB_SleepStatus
      00620B E0               [24] 3419 	movx	a,@dptr
      00620C 30 E1 07         [24] 3420 	jnb	acc.1,00184$
      00620F 12 61 60         [24] 3421 	lcall	_USB_WakeUp_PC
      006212 75 82 00         [24] 3422 	mov	dpl, #0x00
      006215 22               [24] 3423 	ret
                                   3424 ;	tmk_core/protocol/ch555/usb_ak820.c:466: while ((EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_ACK && timeout--) wait_us(40);
      006216                       3425 00184$:
      006216 7F FA            [12] 3426 	mov	r7,#0xfa
      006218                       3427 00127$:
      006218 90 06 F4         [24] 3428 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      00621B E0               [24] 3429 	movx	a,@dptr
      00621C F5 29            [12] 3430 	mov	_ak820_usb_send_sloc1_1_0, a
      00621E 75 2A 00         [24] 3431 	mov	(_ak820_usb_send_sloc1_1_0 + 1),#0x00
      006221 AA 29            [24] 3432 	mov	r2,_ak820_usb_send_sloc1_1_0
      006223 74 22            [12] 3433 	mov	a,#0x22
      006225 25 2A            [12] 3434 	add	a, (_ak820_usb_send_sloc1_1_0 + 1)
      006227 FB               [12] 3435 	mov	r3,a
      006228 8A 82            [24] 3436 	mov	dpl,r2
      00622A 8B 83            [24] 3437 	mov	dph,r3
      00622C E0               [24] 3438 	movx	a,@dptr
      00622D 54 03            [12] 3439 	anl	a,#0x03
      00622F 70 20            [24] 3440 	jnz	00129$
      006231 8F 03            [24] 3441 	mov	ar3,r7
      006233 1F               [12] 3442 	dec	r7
      006234 EB               [12] 3443 	mov	a,r3
      006235 60 1A            [24] 3444 	jz	00129$
      006237 7B 28            [12] 3445 	mov	r3,#0x28
      006239                       3446 00141$:
      006239 EB               [12] 3447 	mov	a,r3
      00623A 60 DC            [24] 3448 	jz	00127$
      00623C 90 00 01         [24] 3449 	mov	dptr,#0x0001
      00623F C0 07            [24] 3450 	push	ar7
      006241 C0 06            [24] 3451 	push	ar6
      006243 C0 03            [24] 3452 	push	ar3
      006245 12 52 22         [24] 3453 	lcall	_mDelayuS
      006248 D0 03            [24] 3454 	pop	ar3
      00624A D0 06            [24] 3455 	pop	ar6
      00624C D0 07            [24] 3456 	pop	ar7
      00624E 1B               [12] 3457 	dec	r3
      00624F 80 E8            [24] 3458 	sjmp	00141$
      006251                       3459 00129$:
                                   3460 ;	tmk_core/protocol/ch555/usb_ak820.c:467: saved_ea = EA;
      006251 A2 AF            [12] 3461 	mov	c,_EA
      006253 E4               [12] 3462 	clr	a
      006254 33               [12] 3463 	rlc	a
      006255 FF               [12] 3464 	mov	r7,a
                                   3465 ;	tmk_core/protocol/ch555/usb_ak820.c:468: EA = 0;
                                   3466 ;	assignBit
      006256 C2 AF            [12] 3467 	clr	_EA
                                   3468 ;	tmk_core/protocol/ch555/usb_ak820.c:469: if (!USB_EnumStatus || (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) != UEP_X_RES_NAK ||
      006258 90 06 8C         [24] 3469 	mov	dptr,#_USB_EnumStatus
      00625B E0               [24] 3470 	movx	a,@dptr
      00625C 60 25            [24] 3471 	jz	00130$
      00625E 90 06 F4         [24] 3472 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      006261 E0               [24] 3473 	movx	a,@dptr
      006262 FB               [12] 3474 	mov	r3,a
      006263 F9               [12] 3475 	mov	r1,a
      006264 7A 00            [12] 3476 	mov	r2,#0x00
      006266 74 22            [12] 3477 	mov	a,#0x22
      006268 2A               [12] 3478 	add	a, r2
      006269 FA               [12] 3479 	mov	r2,a
      00626A 89 82            [24] 3480 	mov	dpl,r1
      00626C 8A 83            [24] 3481 	mov	dph,r2
      00626E E0               [24] 3482 	movx	a,@dptr
      00626F FA               [12] 3483 	mov	r2,a
      006270 53 02 03         [24] 3484 	anl	ar2,#0x03
      006273 BA 02 0D         [24] 3485 	cjne	r2,#0x02,00130$
                                   3486 ;	tmk_core/protocol/ch555/usb_ak820.c:470: (endpoint == RAW_IN_EPNUM && raw_state != RAW_WORK)) { EA = saved_ea; return false; }
      006276 BB 03 13         [24] 3487 	cjne	r3,#0x03,00192$
      006279 90 06 93         [24] 3488 	mov	dptr,#_raw_state
      00627C E0               [24] 3489 	movx	a,@dptr
      00627D FB               [12] 3490 	mov	r3,a
      00627E BB 03 02         [24] 3491 	cjne	r3,#0x03,00331$
      006281 80 09            [24] 3492 	sjmp	00192$
      006283                       3493 00331$:
      006283                       3494 00130$:
                                   3495 ;	assignBit
      006283 EF               [12] 3496 	mov	a,r7
      006284 24 FF            [12] 3497 	add	a,#0xff
      006286 92 AF            [24] 3498 	mov	_EA,c
      006288 75 82 00         [24] 3499 	mov	dpl, #0x00
      00628B 22               [24] 3500 	ret
                                   3501 ;	tmk_core/protocol/ch555/usb_ak820.c:471: for (i = 0; i < length; ++i) {
      00628C                       3502 00192$:
      00628C 90 06 F1         [24] 3503 	mov	dptr,#_ak820_usb_send_PARM_2
      00628F E0               [24] 3504 	movx	a,@dptr
      006290 F5 2B            [12] 3505 	mov	_ak820_usb_send_sloc2_1_0,a
      006292 A3               [24] 3506 	inc	dptr
      006293 E0               [24] 3507 	movx	a,@dptr
      006294 F5 2C            [12] 3508 	mov	(_ak820_usb_send_sloc2_1_0 + 1),a
      006296 90 06 F5         [24] 3509 	mov	dptr,#_ak820_usb_send_offset_10000_413
      006299 E0               [24] 3510 	movx	a,@dptr
      00629A F9               [12] 3511 	mov	r1,a
      00629B B9 2E 03         [24] 3512 	cjne	r1,#0x2e,00332$
      00629E D3               [12] 3513 	setb	c
      00629F 80 01            [24] 3514 	sjmp	00333$
      0062A1                       3515 00332$:
      0062A1 C3               [12] 3516 	clr	c
      0062A2                       3517 00333$:
      0062A2 92 0A            [24] 3518 	mov	_ak820_usb_send_sloc0_1_0,c
      0062A4 78 00            [12] 3519 	mov	r0,#0x00
      0062A6                       3520 00144$:
      0062A6 C3               [12] 3521 	clr	c
      0062A7 E8               [12] 3522 	mov	a,r0
      0062A8 9E               [12] 3523 	subb	a,r6
      0062A9 50 54            [24] 3524 	jnc	00137$
                                   3525 ;	tmk_core/protocol/ch555/usb_ak820.c:472: pUSB_BUF_DEV0[((uint16_t)endpoint << 6) + i] = report[i];
      0062AB C0 07            [24] 3526 	push	ar7
      0062AD 90 06 F4         [24] 3527 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      0062B0 E0               [24] 3528 	movx	a,@dptr
      0062B1 FD               [12] 3529 	mov	r5,a
      0062B2 E4               [12] 3530 	clr	a
      0062B3 C3               [12] 3531 	clr	c
      0062B4 CD               [12] 3532 	xch	a,r5
      0062B5 13               [12] 3533 	rrc	a
      0062B6 CD               [12] 3534 	xch	a,r5
      0062B7 13               [12] 3535 	rrc	a
      0062B8 A2 E0            [12] 3536 	mov	c,acc.0
      0062BA CD               [12] 3537 	xch	a,r5
      0062BB 13               [12] 3538 	rrc	a
      0062BC CD               [12] 3539 	xch	a,r5
      0062BD 13               [12] 3540 	rrc	a
      0062BE CD               [12] 3541 	xch	a,r5
      0062BF FF               [12] 3542 	mov	r7,a
      0062C0 88 03            [24] 3543 	mov	ar3,r0
      0062C2 7C 00            [12] 3544 	mov	r4,#0x00
      0062C4 EB               [12] 3545 	mov	a,r3
      0062C5 2D               [12] 3546 	add	a, r5
      0062C6 FD               [12] 3547 	mov	r5,a
      0062C7 EC               [12] 3548 	mov	a,r4
      0062C8 3F               [12] 3549 	addc	a, r7
      0062C9 24 10            [12] 3550 	add	a,#0x10
      0062CB FF               [12] 3551 	mov	r7,a
      0062CC E8               [12] 3552 	mov	a,r0
      0062CD 25 2B            [12] 3553 	add	a, _ak820_usb_send_sloc2_1_0
      0062CF F5 2D            [12] 3554 	mov	_ak820_usb_send_sloc3_1_0,a
      0062D1 E4               [12] 3555 	clr	a
      0062D2 35 2C            [12] 3556 	addc	a, (_ak820_usb_send_sloc2_1_0 + 1)
      0062D4 F5 2E            [12] 3557 	mov	(_ak820_usb_send_sloc3_1_0 + 1),a
      0062D6 85 2D 82         [24] 3558 	mov	dpl,_ak820_usb_send_sloc3_1_0
      0062D9 85 2E 83         [24] 3559 	mov	dph,(_ak820_usb_send_sloc3_1_0 + 1)
      0062DC E0               [24] 3560 	movx	a,@dptr
      0062DD 8D 82            [24] 3561 	mov	dpl,r5
      0062DF 8F 83            [24] 3562 	mov	dph,r7
      0062E1 F0               [24] 3563 	movx	@dptr,a
                                   3564 ;	tmk_core/protocol/ch555/usb_ak820.c:473: if (offset != SNAPSHOT_SIZE) input_snapshot[offset + i] = report[i];
      0062E2 D0 07            [24] 3565 	pop	ar7
      0062E4 20 0A 15         [24] 3566 	jb	_ak820_usb_send_sloc0_1_0,00145$
      0062E7 E8               [12] 3567 	mov	a,r0
      0062E8 29               [12] 3568 	add	a, r1
      0062E9 24 B6            [12] 3569 	add	a, #_input_snapshot
      0062EB FC               [12] 3570 	mov	r4,a
      0062EC E4               [12] 3571 	clr	a
      0062ED 34 06            [12] 3572 	addc	a,#(_input_snapshot >> 8)
      0062EF FD               [12] 3573 	mov	r5,a
      0062F0 85 2D 82         [24] 3574 	mov	dpl,_ak820_usb_send_sloc3_1_0
      0062F3 85 2E 83         [24] 3575 	mov	dph,(_ak820_usb_send_sloc3_1_0 + 1)
      0062F6 E0               [24] 3576 	movx	a,@dptr
      0062F7 8C 82            [24] 3577 	mov	dpl,r4
      0062F9 8D 83            [24] 3578 	mov	dph,r5
      0062FB F0               [24] 3579 	movx	@dptr,a
      0062FC                       3580 00145$:
                                   3581 ;	tmk_core/protocol/ch555/usb_ak820.c:471: for (i = 0; i < length; ++i) {
      0062FC 08               [12] 3582 	inc	r0
      0062FD 80 A7            [24] 3583 	sjmp	00144$
      0062FF                       3584 00137$:
                                   3585 ;	tmk_core/protocol/ch555/usb_ak820.c:475: EP_LENGTH(endpoint) = length;
      0062FF 90 06 F4         [24] 3586 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      006302 E0               [24] 3587 	movx	a,@dptr
      006303 FD               [12] 3588 	mov	r5,a
      006304 FC               [12] 3589 	mov	r4,a
      006305 7B 00            [12] 3590 	mov	r3,#0x00
      006307 74 08            [12] 3591 	mov	a,#0x08
      006309 2C               [12] 3592 	add	a, r4
      00630A FC               [12] 3593 	mov	r4,a
      00630B 74 22            [12] 3594 	mov	a,#0x22
      00630D 3B               [12] 3595 	addc	a, r3
      00630E FB               [12] 3596 	mov	r3,a
      00630F 8C 82            [24] 3597 	mov	dpl,r4
      006311 8B 83            [24] 3598 	mov	dph,r3
      006313 EE               [12] 3599 	mov	a,r6
      006314 F0               [24] 3600 	movx	@dptr,a
                                   3601 ;	tmk_core/protocol/ch555/usb_ak820.c:476: if (endpoint == RAW_IN_EPNUM) raw_state = RAW_TX_ACTIVE;
      006315 BD 03 06         [24] 3602 	cjne	r5,#0x03,00139$
      006318 90 06 93         [24] 3603 	mov	dptr,#_raw_state
      00631B 74 04            [12] 3604 	mov	a,#0x04
      00631D F0               [24] 3605 	movx	@dptr,a
      00631E                       3606 00139$:
                                   3607 ;	tmk_core/protocol/ch555/usb_ak820.c:477: EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_ACK;
      00631E AD 29            [24] 3608 	mov	r5,_ak820_usb_send_sloc1_1_0
      006320 74 22            [12] 3609 	mov	a,#0x22
      006322 25 2A            [12] 3610 	add	a, (_ak820_usb_send_sloc1_1_0 + 1)
      006324 FE               [12] 3611 	mov	r6,a
      006325 8D 82            [24] 3612 	mov	dpl,r5
      006327 8E 83            [24] 3613 	mov	dph,r6
      006329 E0               [24] 3614 	movx	a,@dptr
      00632A FC               [12] 3615 	mov	r4,a
      00632B 53 04 FC         [24] 3616 	anl	ar4,#0xfc
      00632E 8D 82            [24] 3617 	mov	dpl,r5
      006330 8E 83            [24] 3618 	mov	dph,r6
      006332 EC               [12] 3619 	mov	a,r4
      006333 F0               [24] 3620 	movx	@dptr,a
                                   3621 ;	tmk_core/protocol/ch555/usb_ak820.c:478: EA = saved_ea;
                                   3622 ;	assignBit
      006334 EF               [12] 3623 	mov	a,r7
      006335 24 FF            [12] 3624 	add	a,#0xff
      006337 92 AF            [24] 3625 	mov	_EA,c
                                   3626 ;	tmk_core/protocol/ch555/usb_ak820.c:479: return true;
      006339 75 82 01         [24] 3627 	mov	dpl, #0x01
                                   3628 ;	tmk_core/protocol/ch555/usb_ak820.c:480: }
      00633C 22               [24] 3629 	ret
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
      00633D                       3643 _ak820_usb_try_send:
      00633D E5 82            [12] 3644 	mov	a,dpl
      00633F 90 06 F9         [24] 3645 	mov	dptr,#_ak820_usb_try_send_endpoint_10000_433
      006342 F0               [24] 3646 	movx	@dptr,a
                                   3647 ;	tmk_core/protocol/ch555/usb_ak820.c:483: uint8_t saved_ea = EA;
                                   3648 ;	assignBit
      006343 A2 AF            [12] 3649 	mov	c,_EA
      006345 92 0B            [24] 3650 	mov	_ak820_usb_try_send_sloc0_1_0,c
                                   3651 ;	tmk_core/protocol/ch555/usb_ak820.c:484: bool sent = false;
      006347 90 06 FA         [24] 3652 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      00634A E4               [12] 3653 	clr	a
      00634B F0               [24] 3654 	movx	@dptr,a
                                   3655 ;	tmk_core/protocol/ch555/usb_ak820.c:485: EA = 0;
                                   3656 ;	assignBit
      00634C C2 AF            [12] 3657 	clr	_EA
                                   3658 ;	tmk_core/protocol/ch555/usb_ak820.c:489: if (endpoint >= 1 && endpoint <= 2 && USB_EnumStatus &&
      00634E 90 06 F9         [24] 3659 	mov	dptr,#_ak820_usb_try_send_endpoint_10000_433
      006351 E0               [24] 3660 	movx	a,@dptr
      006352 FF               [12] 3661 	mov	r7,a
      006353 BF 01 00         [24] 3662 	cjne	r7,#0x01,00152$
      006356                       3663 00152$:
      006356 40 4E            [24] 3664 	jc	00102$
      006358 EF               [12] 3665 	mov	a,r7
      006359 24 FD            [12] 3666 	add	a,#0xff - 0x02
      00635B 40 49            [24] 3667 	jc	00102$
                                   3668 ;	free result
      00635D 90 06 8C         [24] 3669 	mov	dptr,#_USB_EnumStatus
      006360 E0               [24] 3670 	movx	a,@dptr
      006361 60 43            [24] 3671 	jz	00102$
                                   3672 ;	tmk_core/protocol/ch555/usb_ak820.c:490: !(USB_SleepStatus & 2) && !keyboard_reset &&
      006363 90 06 8D         [24] 3673 	mov	dptr,#_USB_SleepStatus
      006366 E0               [24] 3674 	movx	a,@dptr
      006367 20 E1 3C         [24] 3675 	jb	acc.1,00102$
      00636A 90 06 B5         [24] 3676 	mov	dptr,#_keyboard_reset
      00636D E0               [24] 3677 	movx	a,@dptr
                                   3678 ;	tmk_core/protocol/ch555/usb_ak820.c:491: (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_NAK) {
      00636E 70 36            [24] 3679 	jnz	00102$
      006370 8F 06            [24] 3680 	mov	ar6,r7
      006372 24 22            [12] 3681 	add	a,#0x22
      006374 FD               [12] 3682 	mov	r5,a
      006375 8E 82            [24] 3683 	mov	dpl,r6
      006377 8D 83            [24] 3684 	mov	dph,r5
      006379 E0               [24] 3685 	movx	a,@dptr
      00637A FE               [12] 3686 	mov	r6,a
      00637B 53 06 03         [24] 3687 	anl	ar6,#0x03
      00637E BE 02 25         [24] 3688 	cjne	r6,#0x02,00102$
                                   3689 ;	tmk_core/protocol/ch555/usb_ak820.c:492: sent = ak820_usb_send(endpoint, report, length);
      006381 90 06 F6         [24] 3690 	mov	dptr,#_ak820_usb_try_send_PARM_2
      006384 E0               [24] 3691 	movx	a,@dptr
      006385 FD               [12] 3692 	mov	r5,a
      006386 A3               [24] 3693 	inc	dptr
      006387 E0               [24] 3694 	movx	a,@dptr
      006388 FE               [12] 3695 	mov	r6,a
      006389 90 06 F8         [24] 3696 	mov	dptr,#_ak820_usb_try_send_PARM_3
      00638C E0               [24] 3697 	movx	a,@dptr
      00638D FC               [12] 3698 	mov	r4,a
      00638E 90 06 F1         [24] 3699 	mov	dptr,#_ak820_usb_send_PARM_2
      006391 ED               [12] 3700 	mov	a,r5
      006392 F0               [24] 3701 	movx	@dptr,a
      006393 EE               [12] 3702 	mov	a,r6
      006394 A3               [24] 3703 	inc	dptr
      006395 F0               [24] 3704 	movx	@dptr,a
      006396 90 06 F3         [24] 3705 	mov	dptr,#_ak820_usb_send_PARM_3
      006399 EC               [12] 3706 	mov	a,r4
      00639A F0               [24] 3707 	movx	@dptr,a
      00639B 8F 82            [24] 3708 	mov	dpl, r7
      00639D 12 61 8B         [24] 3709 	lcall	_ak820_usb_send
      0063A0 E5 82            [12] 3710 	mov	a, dpl
      0063A2 90 06 FA         [24] 3711 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      0063A5 F0               [24] 3712 	movx	@dptr,a
      0063A6                       3713 00102$:
                                   3714 ;	tmk_core/protocol/ch555/usb_ak820.c:494: EA = saved_ea;
                                   3715 ;	assignBit
      0063A6 A2 0B            [12] 3716 	mov	c,_ak820_usb_try_send_sloc0_1_0
      0063A8 92 AF            [24] 3717 	mov	_EA,c
                                   3718 ;	tmk_core/protocol/ch555/usb_ak820.c:495: return sent;
      0063AA 90 06 FA         [24] 3719 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      0063AD E0               [24] 3720 	movx	a,@dptr
                                   3721 ;	tmk_core/protocol/ch555/usb_ak820.c:496: }
      0063AE F5 82            [12] 3722 	mov	dpl,a
      0063B0 22               [24] 3723 	ret
                                   3724 ;------------------------------------------------------------
                                   3725 ;Allocation info for local variables in function 'raw_request_is_nonpersistent'
                                   3726 ;------------------------------------------------------------
                                   3727 ;	tmk_core/protocol/ch555/usb_ak820.c:501: static bool raw_request_is_nonpersistent(void) {
                                   3728 ;	-----------------------------------------
                                   3729 ;	 function raw_request_is_nonpersistent
                                   3730 ;	-----------------------------------------
      0063B1                       3731 _raw_request_is_nonpersistent:
                                   3732 ;	tmk_core/protocol/ch555/usb_ak820.c:502: switch (raw_buffer[0]) {
      0063B1 90 06 94         [24] 3733 	mov	dptr,#_raw_buffer
      0063B4 E0               [24] 3734 	movx	a,@dptr
      0063B5 FF               [12] 3735 	mov	r7,a
      0063B6 BF 01 02         [24] 3736 	cjne	r7,#0x01,00302$
      0063B9 80 35            [24] 3737 	sjmp	00108$
      0063BB                       3738 00302$:
      0063BB BF 02 02         [24] 3739 	cjne	r7,#0x02,00303$
      0063BE 80 34            [24] 3740 	sjmp	00109$
      0063C0                       3741 00303$:
      0063C0 BF 04 02         [24] 3742 	cjne	r7,#0x04,00304$
      0063C3 80 2B            [24] 3743 	sjmp	00108$
      0063C5                       3744 00304$:
      0063C5 BF 08 02         [24] 3745 	cjne	r7,#0x08,00305$
      0063C8 80 49            [24] 3746 	sjmp	00116$
      0063CA                       3747 00305$:
      0063CA BF 0B 02         [24] 3748 	cjne	r7,#0x0b,00306$
      0063CD 80 21            [24] 3749 	sjmp	00108$
      0063CF                       3750 00306$:
      0063CF BF 0C 02         [24] 3751 	cjne	r7,#0x0c,00307$
      0063D2 80 1C            [24] 3752 	sjmp	00108$
      0063D4                       3753 00307$:
      0063D4 BF 0D 02         [24] 3754 	cjne	r7,#0x0d,00308$
      0063D7 80 17            [24] 3755 	sjmp	00108$
      0063D9                       3756 00308$:
      0063D9 BF 0E 02         [24] 3757 	cjne	r7,#0x0e,00309$
      0063DC 80 12            [24] 3758 	sjmp	00108$
      0063DE                       3759 00309$:
      0063DE BF 11 02         [24] 3760 	cjne	r7,#0x11,00310$
      0063E1 80 0D            [24] 3761 	sjmp	00108$
      0063E3                       3762 00310$:
      0063E3 BF 12 02         [24] 3763 	cjne	r7,#0x12,00311$
      0063E6 80 08            [24] 3764 	sjmp	00108$
      0063E8                       3765 00311$:
      0063E8 BF FE 02         [24] 3766 	cjne	r7,#0xfe,00312$
      0063EB 80 4A            [24] 3767 	sjmp	00124$
      0063ED                       3768 00312$:
      0063ED 02 64 8E         [24] 3769 	ljmp	00144$
                                   3770 ;	tmk_core/protocol/ch555/usb_ak820.c:510: case id_bootloader_jump:
      0063F0                       3771 00108$:
                                   3772 ;	tmk_core/protocol/ch555/usb_ak820.c:511: return true;
      0063F0 75 82 01         [24] 3773 	mov	dpl, #0x01
      0063F3 22               [24] 3774 	ret
                                   3775 ;	tmk_core/protocol/ch555/usb_ak820.c:512: case id_get_keyboard_value:
      0063F4                       3776 00109$:
                                   3777 ;	tmk_core/protocol/ch555/usb_ak820.c:513: switch (raw_buffer[1]) {
      0063F4 90 06 95         [24] 3778 	mov	dptr,#(_raw_buffer + 0x0001)
      0063F7 E0               [24] 3779 	movx	a,@dptr
      0063F8 FF               [12] 3780 	mov	r7,a
      0063F9 BF 01 02         [24] 3781 	cjne	r7,#0x01,00313$
      0063FC 80 0D            [24] 3782 	sjmp	00113$
      0063FE                       3783 00313$:
      0063FE BF 02 02         [24] 3784 	cjne	r7,#0x02,00314$
      006401 80 08            [24] 3785 	sjmp	00113$
      006403                       3786 00314$:
      006403 BF 03 02         [24] 3787 	cjne	r7,#0x03,00315$
      006406 80 03            [24] 3788 	sjmp	00113$
      006408                       3789 00315$:
      006408 BF 04 04         [24] 3790 	cjne	r7,#0x04,00114$
                                   3791 ;	tmk_core/protocol/ch555/usb_ak820.c:517: case id_firmware_version:
      00640B                       3792 00113$:
                                   3793 ;	tmk_core/protocol/ch555/usb_ak820.c:518: return true;
      00640B 75 82 01         [24] 3794 	mov	dpl, #0x01
      00640E 22               [24] 3795 	ret
                                   3796 ;	tmk_core/protocol/ch555/usb_ak820.c:519: default: return false;
      00640F                       3797 00114$:
      00640F 75 82 00         [24] 3798 	mov	dpl, #0x00
      006412 22               [24] 3799 	ret
                                   3800 ;	tmk_core/protocol/ch555/usb_ak820.c:521: case id_lighting_get_value:
      006413                       3801 00116$:
                                   3802 ;	tmk_core/protocol/ch555/usb_ak820.c:522: switch (raw_buffer[1]) {
      006413 90 06 95         [24] 3803 	mov	dptr,#(_raw_buffer + 0x0001)
      006416 E0               [24] 3804 	movx	a,@dptr
      006417 FF               [12] 3805 	mov	r7,a
      006418 BF 40 02         [24] 3806 	cjne	r7,#0x40,00318$
      00641B 80 12            [24] 3807 	sjmp	00121$
      00641D                       3808 00318$:
      00641D BF 41 02         [24] 3809 	cjne	r7,#0x41,00319$
      006420 80 0D            [24] 3810 	sjmp	00121$
      006422                       3811 00319$:
      006422 BF 42 02         [24] 3812 	cjne	r7,#0x42,00320$
      006425 80 08            [24] 3813 	sjmp	00121$
      006427                       3814 00320$:
      006427 BF 43 02         [24] 3815 	cjne	r7,#0x43,00321$
      00642A 80 03            [24] 3816 	sjmp	00121$
      00642C                       3817 00321$:
      00642C BF 44 04         [24] 3818 	cjne	r7,#0x44,00122$
                                   3819 ;	tmk_core/protocol/ch555/usb_ak820.c:527: case vialrgb_get_led_info:
      00642F                       3820 00121$:
                                   3821 ;	tmk_core/protocol/ch555/usb_ak820.c:528: return true;
      00642F 75 82 01         [24] 3822 	mov	dpl, #0x01
                                   3823 ;	tmk_core/protocol/ch555/usb_ak820.c:529: default: return false;
      006432 22               [24] 3824 	ret
      006433                       3825 00122$:
      006433 75 82 00         [24] 3826 	mov	dpl, #0x00
                                   3827 ;	tmk_core/protocol/ch555/usb_ak820.c:531: case id_vial_prefix:
      006436 22               [24] 3828 	ret
      006437                       3829 00124$:
                                   3830 ;	tmk_core/protocol/ch555/usb_ak820.c:532: switch (raw_buffer[1]) {
      006437 90 06 95         [24] 3831 	mov	dptr,#(_raw_buffer + 0x0001)
      00643A E0               [24] 3832 	movx	a,@dptr
      00643B FF               [12] 3833 	mov  r7,a
      00643C 24 F2            [12] 3834 	add	a,#0xff - 0x0d
      00643E 40 4A            [24] 3835 	jc	00142$
                                   3836 ;	free result
      006440 EF               [12] 3837 	mov	a,r7
      006441 24 0A            [12] 3838 	add	a,#(00325$-3-.)
      006443 83               [24] 3839 	movc	a,@a+pc
      006444 F5 82            [12] 3840 	mov	dpl,a
      006446 EF               [12] 3841 	mov	a,r7
      006447 24 12            [12] 3842 	add	a,#(00326$-3-.)
      006449 83               [24] 3843 	movc	a,@a+pc
      00644A F5 83            [12] 3844 	mov	dph,a
      00644C E4               [12] 3845 	clr	a
      00644D 73               [24] 3846 	jmp	@a+dptr
      00644E                       3847 00325$:
      00644E 6A                    3848 	.db	00134$
      00644F 6A                    3849 	.db	00134$
      006450 6A                    3850 	.db	00134$
      006451 6A                    3851 	.db	00134$
      006452 8A                    3852 	.db	00142$
      006453 6A                    3853 	.db	00134$
      006454 6A                    3854 	.db	00134$
      006455 6A                    3855 	.db	00134$
      006456 6A                    3856 	.db	00134$
      006457 6A                    3857 	.db	00134$
      006458 6A                    3858 	.db	00134$
      006459 8A                    3859 	.db	00142$
      00645A 8A                    3860 	.db	00142$
      00645B 6E                    3861 	.db	00135$
      00645C                       3862 00326$:
      00645C 64                    3863 	.db	00134$>>8
      00645D 64                    3864 	.db	00134$>>8
      00645E 64                    3865 	.db	00134$>>8
      00645F 64                    3866 	.db	00134$>>8
      006460 64                    3867 	.db	00142$>>8
      006461 64                    3868 	.db	00134$>>8
      006462 64                    3869 	.db	00134$>>8
      006463 64                    3870 	.db	00134$>>8
      006464 64                    3871 	.db	00134$>>8
      006465 64                    3872 	.db	00134$>>8
      006466 64                    3873 	.db	00134$>>8
      006467 64                    3874 	.db	00142$>>8
      006468 64                    3875 	.db	00142$>>8
      006469 64                    3876 	.db	00135$>>8
                                   3877 ;	tmk_core/protocol/ch555/usb_ak820.c:542: case vial_qmk_settings_get:
      00646A                       3878 00134$:
                                   3879 ;	tmk_core/protocol/ch555/usb_ak820.c:543: return true;
      00646A 75 82 01         [24] 3880 	mov	dpl, #0x01
                                   3881 ;	tmk_core/protocol/ch555/usb_ak820.c:544: case vial_dynamic_entry_op:
      00646D 22               [24] 3882 	ret
      00646E                       3883 00135$:
                                   3884 ;	tmk_core/protocol/ch555/usb_ak820.c:545: switch (raw_buffer[2]) {
      00646E 90 06 96         [24] 3885 	mov	dptr,#(_raw_buffer + 0x0002)
      006471 E0               [24] 3886 	movx	a,@dptr
      006472 FF               [12] 3887 	mov	r7,a
      006473 60 0D            [24] 3888 	jz	00139$
      006475 BF 01 02         [24] 3889 	cjne	r7,#0x01,00328$
      006478 80 08            [24] 3890 	sjmp	00139$
      00647A                       3891 00328$:
      00647A BF 03 02         [24] 3892 	cjne	r7,#0x03,00329$
      00647D 80 03            [24] 3893 	sjmp	00139$
      00647F                       3894 00329$:
      00647F BF 05 04         [24] 3895 	cjne	r7,#0x05,00140$
                                   3896 ;	tmk_core/protocol/ch555/usb_ak820.c:549: case dynamic_vial_key_override_get:
      006482                       3897 00139$:
                                   3898 ;	tmk_core/protocol/ch555/usb_ak820.c:550: return true;
      006482 75 82 01         [24] 3899 	mov	dpl, #0x01
                                   3900 ;	tmk_core/protocol/ch555/usb_ak820.c:551: default: return false;
      006485 22               [24] 3901 	ret
      006486                       3902 00140$:
      006486 75 82 00         [24] 3903 	mov	dpl, #0x00
                                   3904 ;	tmk_core/protocol/ch555/usb_ak820.c:553: default: return false;
      006489 22               [24] 3905 	ret
      00648A                       3906 00142$:
      00648A 75 82 00         [24] 3907 	mov	dpl, #0x00
                                   3908 ;	tmk_core/protocol/ch555/usb_ak820.c:555: default: return false;
      00648D 22               [24] 3909 	ret
      00648E                       3910 00144$:
      00648E 75 82 00         [24] 3911 	mov	dpl, #0x00
                                   3912 ;	tmk_core/protocol/ch555/usb_ak820.c:556: }
                                   3913 ;	tmk_core/protocol/ch555/usb_ak820.c:557: }
      006491 22               [24] 3914 	ret
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
      006492                       3925 _ak820_usb_raw_send:
      006492 AF F0            [24] 3926 	mov	r7,b
      006494 AE 83            [24] 3927 	mov	r6,dph
      006496 E5 82            [12] 3928 	mov	a,dpl
      006498 90 06 FC         [24] 3929 	mov	dptr,#_ak820_usb_raw_send_report_10000_449
      00649B F0               [24] 3930 	movx	@dptr,a
      00649C EE               [12] 3931 	mov	a,r6
      00649D A3               [24] 3932 	inc	dptr
      00649E F0               [24] 3933 	movx	@dptr,a
      00649F EF               [12] 3934 	mov	a,r7
      0064A0 A3               [24] 3935 	inc	dptr
      0064A1 F0               [24] 3936 	movx	@dptr,a
                                   3937 ;	tmk_core/protocol/ch555/usb_ak820.c:560: if (length != RAW_EPSIZE) return;
      0064A2 90 06 FB         [24] 3938 	mov	dptr,#_ak820_usb_raw_send_PARM_2
      0064A5 E0               [24] 3939 	movx	a,@dptr
      0064A6 FF               [12] 3940 	mov	r7,a
      0064A7 BF 20 2F         [24] 3941 	cjne	r7,#0x20,00106$
                                   3942 ;	tmk_core/protocol/ch555/usb_ak820.c:561: ak820_nvm_flush();
      0064AA C0 07            [24] 3943 	push	ar7
      0064AC 12 3A CB         [24] 3944 	lcall	_ak820_nvm_flush
      0064AF D0 07            [24] 3945 	pop	ar7
                                   3946 ;	tmk_core/protocol/ch555/usb_ak820.c:562: if (raw_reply_without_nvm || ak820_nvm_ok()) ak820_usb_send(RAW_IN_EPNUM, (const uint8_t __xdata *)report, length);
      0064B1 90 06 B4         [24] 3947 	mov	dptr,#_raw_reply_without_nvm
      0064B4 E0               [24] 3948 	movx	a,@dptr
      0064B5 70 07            [24] 3949 	jnz	00103$
      0064B7 12 3A B3         [24] 3950 	lcall	_ak820_nvm_ok
      0064BA E5 82            [12] 3951 	mov	a, dpl
      0064BC 60 1B            [24] 3952 	jz	00106$
      0064BE                       3953 00103$:
      0064BE 90 06 FC         [24] 3954 	mov	dptr,#_ak820_usb_raw_send_report_10000_449
      0064C1 E0               [24] 3955 	movx	a,@dptr
      0064C2 FD               [12] 3956 	mov	r5,a
      0064C3 A3               [24] 3957 	inc	dptr
      0064C4 E0               [24] 3958 	movx	a,@dptr
      0064C5 FE               [12] 3959 	mov	r6,a
      0064C6 90 06 F1         [24] 3960 	mov	dptr,#_ak820_usb_send_PARM_2
      0064C9 ED               [12] 3961 	mov	a,r5
      0064CA F0               [24] 3962 	movx	@dptr,a
      0064CB EE               [12] 3963 	mov	a,r6
      0064CC A3               [24] 3964 	inc	dptr
      0064CD F0               [24] 3965 	movx	@dptr,a
      0064CE 90 06 F3         [24] 3966 	mov	dptr,#_ak820_usb_send_PARM_3
      0064D1 EF               [12] 3967 	mov	a,r7
      0064D2 F0               [24] 3968 	movx	@dptr,a
      0064D3 75 82 03         [24] 3969 	mov	dpl, #0x03
                                   3970 ;	tmk_core/protocol/ch555/usb_ak820.c:563: }
      0064D6 02 61 8B         [24] 3971 	ljmp	_ak820_usb_send
      0064D9                       3972 00106$:
      0064D9 22               [24] 3973 	ret
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
      0064DA                       3987 _ak820_usb_raw_task:
                                   3988 ;	tmk_core/protocol/ch555/usb_ak820.c:569: uint8_t saved_ea = EA;
      0064DA A2 AF            [12] 3989 	mov	c,_EA
      0064DC E4               [12] 3990 	clr	a
      0064DD 33               [12] 3991 	rlc	a
      0064DE FF               [12] 3992 	mov	r7,a
                                   3993 ;	tmk_core/protocol/ch555/usb_ak820.c:570: EA = 0;
                                   3994 ;	assignBit
      0064DF C2 AF            [12] 3995 	clr	_EA
                                   3996 ;	tmk_core/protocol/ch555/usb_ak820.c:571: if (!USB_EnumStatus || raw_state != RAW_READY) { EA = saved_ea; return; }
      0064E1 90 06 8C         [24] 3997 	mov	dptr,#_USB_EnumStatus
      0064E4 E0               [24] 3998 	movx	a,@dptr
      0064E5 60 0A            [24] 3999 	jz	00101$
      0064E7 90 06 93         [24] 4000 	mov	dptr,#_raw_state
      0064EA E0               [24] 4001 	movx	a,@dptr
      0064EB FE               [12] 4002 	mov	r6,a
      0064EC BE 02 02         [24] 4003 	cjne	r6,#0x02,00270$
      0064EF 80 06            [24] 4004 	sjmp	00102$
      0064F1                       4005 00270$:
      0064F1                       4006 00101$:
                                   4007 ;	assignBit
      0064F1 EF               [12] 4008 	mov	a,r7
      0064F2 24 FF            [12] 4009 	add	a,#0xff
      0064F4 92 AF            [24] 4010 	mov	_EA,c
      0064F6 22               [24] 4011 	ret
      0064F7                       4012 00102$:
                                   4013 ;	tmk_core/protocol/ch555/usb_ak820.c:572: raw_state = RAW_WORK;
      0064F7 90 06 93         [24] 4014 	mov	dptr,#_raw_state
      0064FA 74 03            [12] 4015 	mov	a,#0x03
      0064FC F0               [24] 4016 	movx	@dptr,a
                                   4017 ;	tmk_core/protocol/ch555/usb_ak820.c:573: EA = saved_ea;
                                   4018 ;	assignBit
      0064FD EF               [12] 4019 	mov	a,r7
      0064FE 24 FF            [12] 4020 	add	a,#0xff
      006500 92 AF            [24] 4021 	mov	_EA,c
                                   4022 ;	tmk_core/protocol/ch555/usb_ak820.c:574: if (raw_buffer[0] == 0xfd && raw_buffer[1] == 0) {
      006502 90 06 94         [24] 4023 	mov	dptr,#_raw_buffer
      006505 E0               [24] 4024 	movx	a,@dptr
      006506 FF               [12] 4025 	mov	r7,a
      006507 E4               [12] 4026 	clr	a
      006508 BF FD 01         [24] 4027 	cjne	r7,#0xfd,00271$
      00650B 04               [12] 4028 	inc	a
      00650C                       4029 00271$:
      00650C FF               [12] 4030 	mov	r7,a
      00650D 70 03            [24] 4031 	jnz	00273$
      00650F 02 65 C9         [24] 4032 	ljmp	00118$
      006512                       4033 00273$:
      006512 90 06 95         [24] 4034 	mov	dptr,#(_raw_buffer + 0x0001)
      006515 E0               [24] 4035 	movx	a,@dptr
      006516 60 03            [24] 4036 	jz	00274$
      006518 02 65 C9         [24] 4037 	ljmp	00118$
      00651B                       4038 00274$:
                                   4039 ;	tmk_core/protocol/ch555/usb_ak820.c:577: address = ((uint16_t)raw_buffer[2] << 8) | raw_buffer[3];
      00651B 90 06 96         [24] 4040 	mov	dptr,#(_raw_buffer + 0x0002)
      00651E E0               [24] 4041 	movx	a,@dptr
      00651F FD               [12] 4042 	mov	r5,a
      006520 7E 00            [12] 4043 	mov	r6,#0x00
      006522 90 06 97         [24] 4044 	mov	dptr,#(_raw_buffer + 0x0003)
      006525 E0               [24] 4045 	movx	a,@dptr
      006526 7B 00            [12] 4046 	mov	r3,#0x00
      006528 42 06            [12] 4047 	orl	ar6,a
      00652A EB               [12] 4048 	mov	a,r3
      00652B 42 05            [12] 4049 	orl	ar5,a
                                   4050 ;	tmk_core/protocol/ch555/usb_ak820.c:578: length = raw_buffer[4];
      00652D 90 06 98         [24] 4051 	mov	dptr,#(_raw_buffer + 0x0004)
      006530 E0               [24] 4052 	movx	a,@dptr
      006531 FC               [12] 4053 	mov	r4,a
                                   4054 ;	tmk_core/protocol/ch555/usb_ak820.c:579: for (i = 5; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
      006532 7B 05            [12] 4055 	mov	r3,#0x05
      006534                       4056 00128$:
      006534 EB               [12] 4057 	mov	a,r3
      006535 24 94            [12] 4058 	add	a, #_raw_buffer
      006537 F5 82            [12] 4059 	mov	dpl,a
      006539 E4               [12] 4060 	clr	a
      00653A 34 06            [12] 4061 	addc	a, #(_raw_buffer >> 8)
      00653C F5 83            [12] 4062 	mov	dph,a
      00653E E4               [12] 4063 	clr	a
      00653F F0               [24] 4064 	movx	@dptr,a
      006540 0B               [12] 4065 	inc	r3
      006541 BB 20 00         [24] 4066 	cjne	r3,#0x20,00275$
      006544                       4067 00275$:
      006544 40 EE            [24] 4068 	jc	00128$
                                   4069 ;	tmk_core/protocol/ch555/usb_ak820.c:580: if (length > RAW_EPSIZE - 5 || (length && address > 0xffffu - (length - 1))) {
      006546 EC               [12] 4070 	mov	a,r4
      006547 24 E4            [12] 4071 	add	a,#0xff - 0x1b
      006549 40 1C            [24] 4072 	jc	00106$
                                   4073 ;	free result
      00654B EC               [12] 4074 	mov	a,r4
      00654C 60 26            [24] 4075 	jz	00165$
      00654E 8C 03            [24] 4076 	mov	ar3,r4
      006550 1B               [12] 4077 	dec	r3
      006551 7A 00            [12] 4078 	mov	r2,#0x00
      006553 74 FF            [12] 4079 	mov	a,#0xff
      006555 C3               [12] 4080 	clr	c
      006556 9B               [12] 4081 	subb	a,r3
      006557 FB               [12] 4082 	mov	r3,a
      006558 74 FF            [12] 4083 	mov	a,#0xff
      00655A 9A               [12] 4084 	subb	a,r2
      00655B FA               [12] 4085 	mov	r2,a
      00655C 8E 00            [24] 4086 	mov	ar0,r6
      00655E 8D 01            [24] 4087 	mov	ar1,r5
      006560 C3               [12] 4088 	clr	c
      006561 EB               [12] 4089 	mov	a,r3
      006562 98               [12] 4090 	subb	a,r0
      006563 EA               [12] 4091 	mov	a,r2
      006564 99               [12] 4092 	subb	a,r1
      006565 50 0D            [24] 4093 	jnc	00165$
                                   4094 ;	free result
      006567                       4095 00106$:
                                   4096 ;	tmk_core/protocol/ch555/usb_ak820.c:581: raw_buffer[1] = 0xff;
      006567 90 06 95         [24] 4097 	mov	dptr,#(_raw_buffer + 0x0001)
      00656A 74 FF            [12] 4098 	mov	a,#0xff
      00656C F0               [24] 4099 	movx	@dptr,a
                                   4100 ;	tmk_core/protocol/ch555/usb_ak820.c:582: raw_buffer[4] = 0;
      00656D 90 06 98         [24] 4101 	mov	dptr,#(_raw_buffer + 0x0004)
      006570 E4               [12] 4102 	clr	a
      006571 F0               [24] 4103 	movx	@dptr,a
                                   4104 ;	tmk_core/protocol/ch555/usb_ak820.c:584: for (i = 0; i < length; ++i) raw_buffer[5 + i] = READ_CODE(address + i);
      006572 80 3C            [24] 4105 	sjmp	00108$
      006574                       4106 00165$:
      006574 7B 00            [12] 4107 	mov	r3,#0x00
      006576                       4108 00131$:
      006576 C3               [12] 4109 	clr	c
      006577 EB               [12] 4110 	mov	a,r3
      006578 9C               [12] 4111 	subb	a,r4
      006579 50 35            [24] 4112 	jnc	00108$
      00657B C0 04            [24] 4113 	push	ar4
      00657D 8B 02            [24] 4114 	mov	ar2,r3
      00657F 74 05            [12] 4115 	mov	a,#0x05
      006581 2A               [12] 4116 	add	a, r2
      006582 F9               [12] 4117 	mov	r1,a
      006583 33               [12] 4118 	rlc	a
      006584 95 E0            [12] 4119 	subb	a,acc
      006586 FA               [12] 4120 	mov	r2,a
      006587 E9               [12] 4121 	mov	a,r1
      006588 24 94            [12] 4122 	add	a, #_raw_buffer
      00658A F9               [12] 4123 	mov	r1,a
      00658B EA               [12] 4124 	mov	a,r2
      00658C 34 06            [12] 4125 	addc	a, #(_raw_buffer >> 8)
      00658E FA               [12] 4126 	mov	r2,a
      00658F 8B 2F            [24] 4127 	mov	_ak820_usb_raw_task_sloc0_1_0,r3
      006591 75 30 00         [24] 4128 	mov	(_ak820_usb_raw_task_sloc0_1_0 + 1),#0x00
      006594 8E 00            [24] 4129 	mov	ar0,r6
      006596 8D 04            [24] 4130 	mov	ar4,r5
      006598 E5 2F            [12] 4131 	mov	a,_ak820_usb_raw_task_sloc0_1_0
      00659A 28               [12] 4132 	add	a, r0
      00659B F8               [12] 4133 	mov	r0,a
      00659C E5 30            [12] 4134 	mov	a,(_ak820_usb_raw_task_sloc0_1_0 + 1)
      00659E 3C               [12] 4135 	addc	a, r4
      00659F FC               [12] 4136 	mov	r4,a
      0065A0 88 82            [24] 4137 	mov	dpl,r0
      0065A2 8C 83            [24] 4138 	mov	dph,r4
      0065A4 E4               [12] 4139 	clr	a
      0065A5 93               [24] 4140 	movc	a,@a+dptr
      0065A6 89 82            [24] 4141 	mov	dpl,r1
      0065A8 8A 83            [24] 4142 	mov	dph,r2
      0065AA F0               [24] 4143 	movx	@dptr,a
      0065AB 0B               [12] 4144 	inc	r3
      0065AC D0 04            [24] 4145 	pop	ar4
      0065AE 80 C6            [24] 4146 	sjmp	00131$
      0065B0                       4147 00108$:
                                   4148 ;	tmk_core/protocol/ch555/usb_ak820.c:588: ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
      0065B0 90 06 F1         [24] 4149 	mov	dptr,#_ak820_usb_send_PARM_2
      0065B3 74 94            [12] 4150 	mov	a,#_raw_buffer
      0065B5 F0               [24] 4151 	movx	@dptr,a
      0065B6 74 06            [12] 4152 	mov	a,#(_raw_buffer >> 8)
      0065B8 A3               [24] 4153 	inc	dptr
      0065B9 F0               [24] 4154 	movx	@dptr,a
      0065BA 90 06 F3         [24] 4155 	mov	dptr,#_ak820_usb_send_PARM_3
      0065BD 74 20            [12] 4156 	mov	a,#0x20
      0065BF F0               [24] 4157 	movx	@dptr,a
      0065C0 75 82 03         [24] 4158 	mov	dpl, #0x03
      0065C3 12 61 8B         [24] 4159 	lcall	_ak820_usb_send
      0065C6 02 66 89         [24] 4160 	ljmp	00119$
      0065C9                       4161 00118$:
                                   4162 ;	tmk_core/protocol/ch555/usb_ak820.c:589: } else if (raw_buffer[0] == 0xfd && raw_buffer[1] == 1) {
      0065C9 EF               [12] 4163 	mov	a,r7
      0065CA 70 03            [24] 4164 	jnz	00281$
      0065CC 02 66 66         [24] 4165 	ljmp	00114$
      0065CF                       4166 00281$:
      0065CF 90 06 95         [24] 4167 	mov	dptr,#(_raw_buffer + 0x0001)
      0065D2 E0               [24] 4168 	movx	a,@dptr
      0065D3 FF               [12] 4169 	mov	r7,a
      0065D4 BF 01 02         [24] 4170 	cjne	r7,#0x01,00282$
      0065D7 80 03            [24] 4171 	sjmp	00283$
      0065D9                       4172 00282$:
      0065D9 02 66 66         [24] 4173 	ljmp	00114$
      0065DC                       4174 00283$:
                                   4175 ;	tmk_core/protocol/ch555/usb_ak820.c:592: for (i = 2; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
      0065DC 7F 02            [12] 4176 	mov	r7,#0x02
      0065DE                       4177 00133$:
      0065DE EF               [12] 4178 	mov	a,r7
      0065DF 24 94            [12] 4179 	add	a, #_raw_buffer
      0065E1 F5 82            [12] 4180 	mov	dpl,a
      0065E3 E4               [12] 4181 	clr	a
      0065E4 34 06            [12] 4182 	addc	a, #(_raw_buffer >> 8)
      0065E6 F5 83            [12] 4183 	mov	dph,a
      0065E8 E4               [12] 4184 	clr	a
      0065E9 F0               [24] 4185 	movx	@dptr,a
      0065EA 0F               [12] 4186 	inc	r7
      0065EB BF 20 00         [24] 4187 	cjne	r7,#0x20,00284$
      0065EE                       4188 00284$:
      0065EE 40 EE            [24] 4189 	jc	00133$
                                   4190 ;	tmk_core/protocol/ch555/usb_ak820.c:593: raw_buffer[2] = 1;
      0065F0 90 06 96         [24] 4191 	mov	dptr,#(_raw_buffer + 0x0002)
      0065F3 74 01            [12] 4192 	mov	a,#0x01
      0065F5 F0               [24] 4193 	movx	@dptr,a
                                   4194 ;	tmk_core/protocol/ch555/usb_ak820.c:594: raw_buffer[3] = 0xa8;
      0065F6 90 06 97         [24] 4195 	mov	dptr,#(_raw_buffer + 0x0003)
      0065F9 74 A8            [12] 4196 	mov	a,#0xa8
      0065FB F0               [24] 4197 	movx	@dptr,a
                                   4198 ;	tmk_core/protocol/ch555/usb_ak820.c:595: ak820_nvm_diagnostic(&raw_buffer[4]);
      0065FC 90 06 98         [24] 4199 	mov	dptr,#(_raw_buffer + 0x0004)
      0065FF 12 37 C1         [24] 4200 	lcall	_ak820_nvm_diagnostic
                                   4201 ;	tmk_core/protocol/ch555/usb_ak820.c:596: for (i = 0; i < 6; ++i) raw_buffer[11 + i] = ak820_flash_diagnostic[i];
      006602 7F 00            [12] 4202 	mov	r7,#0x00
      006604                       4203 00135$:
      006604 8F 06            [24] 4204 	mov	ar6,r7
      006606 74 0B            [12] 4205 	mov	a,#0x0b
      006608 2E               [12] 4206 	add	a, r6
      006609 24 94            [12] 4207 	add	a,#_raw_buffer
      00660B FE               [12] 4208 	mov	r6,a
      00660C E4               [12] 4209 	clr	a
      00660D 34 06            [12] 4210 	addc	a, #(_raw_buffer >> 8)
      00660F FD               [12] 4211 	mov	r5,a
      006610 EF               [12] 4212 	mov	a,r7
      006611 24 1B            [12] 4213 	add	a, #_ak820_flash_diagnostic
      006613 F5 82            [12] 4214 	mov	dpl,a
      006615 E4               [12] 4215 	clr	a
      006616 34 04            [12] 4216 	addc	a, #(_ak820_flash_diagnostic >> 8)
      006618 F5 83            [12] 4217 	mov	dph,a
      00661A E0               [24] 4218 	movx	a,@dptr
      00661B 8E 82            [24] 4219 	mov	dpl,r6
      00661D 8D 83            [24] 4220 	mov	dph,r5
      00661F F0               [24] 4221 	movx	@dptr,a
      006620 0F               [12] 4222 	inc	r7
      006621 BF 06 00         [24] 4223 	cjne	r7,#0x06,00286$
      006624                       4224 00286$:
      006624 40 DE            [24] 4225 	jc	00135$
                                   4226 ;	tmk_core/protocol/ch555/usb_ak820.c:597: raw_buffer[17] = vial_unlocked;
      006626 90 0C 07         [24] 4227 	mov	dptr,#_vial_unlocked
      006629 E0               [24] 4228 	movx	a,@dptr
      00662A 90 06 A5         [24] 4229 	mov	dptr,#(_raw_buffer + 0x0011)
      00662D F0               [24] 4230 	movx	@dptr,a
                                   4231 ;	tmk_core/protocol/ch555/usb_ak820.c:598: raw_buffer[18] = vial_unlock_in_progress;
      00662E 90 0C 08         [24] 4232 	mov	dptr,#_vial_unlock_in_progress
      006631 E0               [24] 4233 	movx	a,@dptr
      006632 90 06 A6         [24] 4234 	mov	dptr,#(_raw_buffer + 0x0012)
      006635 F0               [24] 4235 	movx	@dptr,a
                                   4236 ;	tmk_core/protocol/ch555/usb_ak820.c:599: raw_buffer[19] = USB_EnumStatus;
      006636 90 06 8C         [24] 4237 	mov	dptr,#_USB_EnumStatus
      006639 E0               [24] 4238 	movx	a,@dptr
      00663A 90 06 A7         [24] 4239 	mov	dptr,#(_raw_buffer + 0x0013)
      00663D F0               [24] 4240 	movx	@dptr,a
                                   4241 ;	tmk_core/protocol/ch555/usb_ak820.c:600: raw_buffer[20] = USB_SleepStatus;
      00663E 90 06 8D         [24] 4242 	mov	dptr,#_USB_SleepStatus
      006641 E0               [24] 4243 	movx	a,@dptr
      006642 90 06 A8         [24] 4244 	mov	dptr,#(_raw_buffer + 0x0014)
      006645 F0               [24] 4245 	movx	@dptr,a
                                   4246 ;	tmk_core/protocol/ch555/usb_ak820.c:601: raw_buffer[21] = raw_state;
      006646 90 06 93         [24] 4247 	mov	dptr,#_raw_state
      006649 E0               [24] 4248 	movx	a,@dptr
      00664A 90 06 A9         [24] 4249 	mov	dptr,#(_raw_buffer + 0x0015)
      00664D F0               [24] 4250 	movx	@dptr,a
                                   4251 ;	tmk_core/protocol/ch555/usb_ak820.c:602: ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
      00664E 90 06 F1         [24] 4252 	mov	dptr,#_ak820_usb_send_PARM_2
      006651 74 94            [12] 4253 	mov	a,#_raw_buffer
      006653 F0               [24] 4254 	movx	@dptr,a
      006654 74 06            [12] 4255 	mov	a,#(_raw_buffer >> 8)
      006656 A3               [24] 4256 	inc	dptr
      006657 F0               [24] 4257 	movx	@dptr,a
      006658 90 06 F3         [24] 4258 	mov	dptr,#_ak820_usb_send_PARM_3
      00665B 74 20            [12] 4259 	mov	a,#0x20
      00665D F0               [24] 4260 	movx	@dptr,a
      00665E 75 82 03         [24] 4261 	mov	dpl, #0x03
      006661 12 61 8B         [24] 4262 	lcall	_ak820_usb_send
      006664 80 23            [24] 4263 	sjmp	00119$
      006666                       4264 00114$:
                                   4265 ;	tmk_core/protocol/ch555/usb_ak820.c:604: raw_reply_without_nvm = raw_request_is_nonpersistent();
      006666 12 63 B1         [24] 4266 	lcall	_raw_request_is_nonpersistent
      006669 E5 82            [12] 4267 	mov	a, dpl
      00666B 90 06 B4         [24] 4268 	mov	dptr,#_raw_reply_without_nvm
      00666E F0               [24] 4269 	movx	@dptr,a
                                   4270 ;	tmk_core/protocol/ch555/usb_ak820.c:605: ak820_nvm_begin();
      00666F 12 3C 64         [24] 4271 	lcall	_ak820_nvm_begin
                                   4272 ;	tmk_core/protocol/ch555/usb_ak820.c:606: raw_hid_receive(raw_buffer, RAW_EPSIZE);
      006672 90 0A 53         [24] 4273 	mov	dptr,#_raw_hid_receive_PARM_2
      006675 74 20            [12] 4274 	mov	a,#0x20
      006677 F0               [24] 4275 	movx	@dptr,a
      006678 90 06 94         [24] 4276 	mov	dptr,#_raw_buffer
      00667B 75 F0 00         [24] 4277 	mov	b, #0x00
      00667E 12 A1 7A         [24] 4278 	lcall	_raw_hid_receive
                                   4279 ;	tmk_core/protocol/ch555/usb_ak820.c:607: ak820_nvm_end();
      006681 12 3C 79         [24] 4280 	lcall	_ak820_nvm_end
                                   4281 ;	tmk_core/protocol/ch555/usb_ak820.c:608: raw_reply_without_nvm = false;
      006684 90 06 B4         [24] 4282 	mov	dptr,#_raw_reply_without_nvm
      006687 E4               [12] 4283 	clr	a
      006688 F0               [24] 4284 	movx	@dptr,a
      006689                       4285 00119$:
                                   4286 ;	tmk_core/protocol/ch555/usb_ak820.c:610: saved_ea = EA;
                                   4287 ;	assignBit
      006689 A2 AF            [12] 4288 	mov	c,_EA
      00668B 92 0C            [24] 4289 	mov	_ak820_usb_raw_task_sloc1_1_0,c
                                   4290 ;	tmk_core/protocol/ch555/usb_ak820.c:611: EA = 0;
                                   4291 ;	assignBit
      00668D C2 AF            [12] 4292 	clr	_EA
                                   4293 ;	tmk_core/protocol/ch555/usb_ak820.c:613: if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_TX_WAIT;
      00668F 90 06 93         [24] 4294 	mov	dptr,#_raw_state
      006692 E0               [24] 4295 	movx	a,@dptr
      006693 FF               [12] 4296 	mov	r7,a
      006694 BF 04 08         [24] 4297 	cjne	r7,#0x04,00126$
      006697 90 06 93         [24] 4298 	mov	dptr,#_raw_state
      00669A 74 05            [12] 4299 	mov	a,#0x05
      00669C F0               [24] 4300 	movx	@dptr,a
      00669D 80 21            [24] 4301 	sjmp	00127$
      00669F                       4302 00126$:
                                   4303 ;	tmk_core/protocol/ch555/usb_ak820.c:614: else if (raw_state == RAW_WORK || raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED) raw_state = RAW_IDLE;
      00669F 90 06 93         [24] 4304 	mov	dptr,#_raw_state
      0066A2 E0               [24] 4305 	movx	a,@dptr
      0066A3 FF               [12] 4306 	mov	r7,a
      0066A4 BF 03 02         [24] 4307 	cjne	r7,#0x03,00290$
      0066A7 80 12            [24] 4308 	sjmp	00121$
      0066A9                       4309 00290$:
      0066A9 90 06 93         [24] 4310 	mov	dptr,#_raw_state
      0066AC E0               [24] 4311 	movx	a,@dptr
      0066AD FF               [12] 4312 	mov	r7,a
      0066AE BF 06 02         [24] 4313 	cjne	r7,#0x06,00291$
      0066B1 80 08            [24] 4314 	sjmp	00121$
      0066B3                       4315 00291$:
      0066B3 90 06 93         [24] 4316 	mov	dptr,#_raw_state
      0066B6 E0               [24] 4317 	movx	a,@dptr
      0066B7 FF               [12] 4318 	mov	r7,a
      0066B8 BF 07 05         [24] 4319 	cjne	r7,#0x07,00127$
      0066BB                       4320 00121$:
      0066BB 90 06 93         [24] 4321 	mov	dptr,#_raw_state
      0066BE E4               [12] 4322 	clr	a
      0066BF F0               [24] 4323 	movx	@dptr,a
      0066C0                       4324 00127$:
                                   4325 ;	tmk_core/protocol/ch555/usb_ak820.c:615: EA = saved_ea;
                                   4326 ;	assignBit
      0066C0 A2 0C            [12] 4327 	mov	c,_ak820_usb_raw_task_sloc1_1_0
      0066C2 92 AF            [24] 4328 	mov	_EA,c
                                   4329 ;	tmk_core/protocol/ch555/usb_ak820.c:616: }
      0066C4 22               [24] 4330 	ret
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
      0066C5                       4341 _ak820_usb_take_keyboard_reset:
                                   4342 ;	tmk_core/protocol/ch555/usb_ak820.c:620: uint8_t saved_ea = EA;
                                   4343 ;	assignBit
      0066C5 A2 AF            [12] 4344 	mov	c,_EA
      0066C7 92 0D            [24] 4345 	mov	_ak820_usb_take_keyboard_reset_sloc0_1_0,c
                                   4346 ;	tmk_core/protocol/ch555/usb_ak820.c:621: EA = 0;
                                   4347 ;	assignBit
      0066C9 C2 AF            [12] 4348 	clr	_EA
                                   4349 ;	tmk_core/protocol/ch555/usb_ak820.c:622: result = keyboard_reset;
      0066CB 90 06 B5         [24] 4350 	mov	dptr,#_keyboard_reset
      0066CE E0               [24] 4351 	movx	a,@dptr
      0066CF FF               [12] 4352 	mov	r7,a
                                   4353 ;	tmk_core/protocol/ch555/usb_ak820.c:623: keyboard_reset = 0;
      0066D0 E4               [12] 4354 	clr	a
      0066D1 F0               [24] 4355 	movx	@dptr,a
                                   4356 ;	tmk_core/protocol/ch555/usb_ak820.c:624: EA = saved_ea;
                                   4357 ;	assignBit
      0066D2 A2 0D            [12] 4358 	mov	c,_ak820_usb_take_keyboard_reset_sloc0_1_0
      0066D4 92 AF            [24] 4359 	mov	_EA,c
                                   4360 ;	tmk_core/protocol/ch555/usb_ak820.c:625: return result != 0;
      0066D6 EF               [12] 4361 	mov	a,r7
      0066D7 B4 01 00         [24] 4362 	cjne	a,#0x01,00103$
      0066DA                       4363 00103$:
      0066DA B3               [12] 4364 	cpl	c
      0066DB 92 0D            [24] 4365 	mov	_ak820_usb_take_keyboard_reset_sloc0_1_0,c
      0066DD E4               [12] 4366 	clr	a
      0066DE 33               [12] 4367 	rlc	a
      0066DF F5 82            [12] 4368 	mov	dpl, a
                                   4369 ;	tmk_core/protocol/ch555/usb_ak820.c:626: }
      0066E1 22               [24] 4370 	ret
                                   4371 	.area CSEG    (CODE)
                                   4372 	.area CONST   (CODE)
                                   4373 	.area CONST   (CODE)
      00B612                       4374 _shared_offsets:
      00B612 00                    4375 	.db #0x00	; 0
      00B613 00                    4376 	.db #0x00	; 0
      00B614 28                    4377 	.db #0x28	; 40
      00B615 28                    4378 	.db #0x28	; 40
      00B616 2B                    4379 	.db #0x2b	; 43
      00B617 00                    4380 	.db #0x00	; 0
      00B618 08                    4381 	.db #0x08	; 8
                                   4382 	.area CSEG    (CODE)
                                   4383 	.area CONST   (CODE)
      00B619                       4384 _shared_lengths:
      00B619 00                    4385 	.db #0x00	; 0
      00B61A 00                    4386 	.db #0x00	; 0
      00B61B 00                    4387 	.db #0x00	; 0
      00B61C 03                    4388 	.db #0x03	; 3
      00B61D 03                    4389 	.db #0x03	; 3
      00B61E 00                    4390 	.db #0x00	; 0
      00B61F 20                    4391 	.db #0x20	; 32
                                   4392 	.area CSEG    (CODE)
                                   4393 	.area XINIT   (CODE)
                                   4394 	.area CABS    (ABS,CODE)
