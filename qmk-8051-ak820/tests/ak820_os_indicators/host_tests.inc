/* Production functions, host MMIO and a controlled 32-bit clock. */
#include "../../keyboards/ajazz/ak820/ak820_os_indicators.c"
static bool caps_word_led_active;
bool is_caps_word_on(void) { return caps_word_led_active; }
#include "../../keyboards/ajazz/ak820/ak820_indicators.c"
static uint32_t os_now;
static unsigned os_clock_reads;
static uint8_t os_first_clock_ea;
uint32_t timer_read32(void) { if (!os_clock_reads++) os_first_clock_ea=EA; return os_now; }
uint16_t timer_read(void) { return (uint16_t)os_now; }
uint32_t timer_elapsed32(uint32_t last) { return os_now-last; }
uint8_t ak820_led_dma[512];
volatile uint8_t IE_PWM_I2C;
layer_state_t layer_state, default_layer_state;
#ifdef AK820_MAC_PC
bool ak820_mac_mode;
#endif

static void os_request(uint8_t action, uint8_t mode, uint8_t status, uint8_t effective) {
    uint8_t packet[32] = {0xfd,2,1,action,mode};
    unsigned old_begins=begins, old_flushes=flushes, old_ends=ends, old_received=received;
    os_clock_reads=0;
    raw_request(packet); ak820_usb_raw_task();
    if (action==1 && status==0) assert(os_clock_reads && os_first_clock_ea==0);
    const volatile uint8_t *p=pUSB_BUF_DEV0+UX_EP3_ADDR;
    assert(raw_state == RAW_TX_WAIT && D0_EP3T_L == 32);
    const uint8_t expected[32]={0xfd,2,1,status,effective,0xa8,0xb8,0x0b,0,0x10};
    assert(!memcmp((const void *)p,expected,32));
    assert(begins==old_begins && flushes==old_flushes && ends==old_ends && received==old_received);
    in(3);
}

static void test_os_indicators(void) {
    fresh(); configure(); vial_unlock_in_progress=0; vial_unlocked=0;
    os_now=100; nvm_good=false;
    os_request(0,0,0,0);
    for (uint8_t irq=0;irq<2;++irq) {
        EA=irq; os_request(1,2,0,2); assert(EA==irq);
    }
    EA=1;
    os_now=3099; os_request(0,0,0,2);
    os_now=3100; os_request(0,0,0,0); /* GET must not renew. */
    os_now=4000; os_request(1,1,0,1);
    /* Every reserved byte and every malformed field must preserve the lease. */
    for (unsigned field=2;field<32;++field) {
        uint8_t packet[32]={0xfd,2,1,1,1};
        packet[field]=field==2?2:field==3?2:field==4?4:1;
        os_now=5000; raw_request(packet); ak820_usb_raw_task();
        assert(raw_state==RAW_TX_WAIT);
        assert(pUSB_BUF_DEV0[UX_EP3_ADDR+3]==1 && pUSB_BUF_DEV0[UX_EP3_ADDR+4]==1);
        in(3);
    }
    for (unsigned field=2;field<=4;++field) for (unsigned value=0;value<256;++value) {
        if ((field==2 && value==1) || (field==3 && value<=1) || (field==4 && value<=3)) continue;
        uint8_t packet[32]={0xfd,2,1,1,1}; packet[field]=value;
        raw_request(packet); ak820_usb_raw_task();
        assert(raw_state==RAW_TX_WAIT);
        assert(pUSB_BUF_DEV0[UX_EP3_ADDR+3]==1 && pUSB_BUF_DEV0[UX_EP3_ADDR+4]==1);
        in(3);
    }
    os_request(0,1,1,1); /* GET with nonzero mode is malformed. */
    os_now=7000; os_request(0,0,0,0);
    os_now=8000; os_request(1,3,0,3);
    /* Boundary fixtures after EP0 acceptance: setter refuses both lost
     * configuration and sleep. Sleeping transport cannot publish its reply. */
    for (unsigned asleep=0;asleep<2;++asleep) {
        const uint8_t packet[32]={0xfd,2,1,1,2};
        raw_request(packet);
        if(asleep) USB_SleepStatus=2; else D0UsbConfig=0;
        ak820_usb_raw_task();
        assert(ak820_os_indicator_get()==3 && raw_buffer[3]==2);
        if(asleep) assert(raw_state==RAW_IDLE && (D0_EP3RES & MASK_UEP_X_RES)==UEP_X_RES_NAK);
        else { assert(raw_state==RAW_TX_WAIT); in(3); }
        USB_SleepStatus=0; D0UsbConfig=1;
    }
    vial_unlock_in_progress=1; os_request(1,2,2,0);
    vial_unlock_in_progress=0; os_request(0,0,0,0);
    os_request(1,2,0,2);
    USB_IF|=bUX_IF_SUSPEND; service_irq();
    assert(ak820_os_indicator_get()==0);
    USB_SleepStatus=0; os_request(1,1,0,1);
    setup(0,USB_SET_CONFIGURATION,1,0,0); in(0);
    assert(ak820_os_indicator_get()==0);
    os_request(1,2,0,2); reset(); assert(ak820_os_indicator_get()==0);
    configure(); os_request(0,0,0,0);
    caps_word_led_active = false;
    /* C and W retain their existing channels; OS owns component 3 only.
     * Shared intensity must keep W full while OS is off or breathing. */
    for (uint8_t irq=0;irq<2;++irq) for (uint8_t mode=0;mode<4;++mode)
    for (uint8_t mac=0;mac<2;++mac) {
        os_now=0x12345400; os_request(1,mode,0,mode);
#ifdef AK820_MAC_PC
        ak820_mac_mode=mac;
#endif
        for (unsigned caps=0;caps<2;++caps) for (unsigned layer=0;layer<2;++layer)
        for (unsigned defaults=0;defaults<2;++defaults) {
            memset(ak820_led_dma,0x69,sizeof(ak820_led_dma));
            IE_PWM_I2C=irq; KB_USB_SetReport=caps?2:0;
            layer_state=layer?2:1; default_layer_state=defaults?4:1;
            ak820_update_indicators();
            uint8_t normal=0;
#ifdef AK820_MAC_PC
            normal=mac?255:0;
#endif
            uint8_t os=mode==0?normal:mode==1?0:mode==2?255:128;
            uint8_t w=(layer||defaults)?255:0;
            assert(ak820_led_dma[0x11c]==(caps?255:0) && ak820_led_dma[0x11d]==(caps?255:0));
            assert(ak820_led_dma[0x13c]==((w||os)?255:0));
            assert(ak820_led_dma[0x13d]==w && ak820_led_dma[0x13f]==os);
            assert(IE_PWM_I2C==irq);
            for (unsigned i=0;i<512;++i) if(i!=0x11c&&i!=0x11d&&i!=0x13c&&i!=0x13d&&i!=0x13f) assert(ak820_led_dma[i]==0x69);
        }
    }
    /* Local Caps Word lights C without modifying the host LED report. */
    KB_USB_SetReport=0; caps_word_led_active=true; ak820_update_indicators();
    assert(ak820_led_dma[0x11c]==255 && ak820_led_dma[0x11d]==255);
    KB_USB_SetReport=2; ak820_update_indicators();
    assert(ak820_led_dma[0x11c]==255 && ak820_led_dma[0x11d]==255);
    caps_word_led_active=false; ak820_update_indicators();
    assert(ak820_led_dma[0x11c]==255 && ak820_led_dma[0x11d]==255);
    KB_USB_SetReport=0; ak820_update_indicators();
    assert(ak820_led_dma[0x11c]==0 && ak820_led_dma[0x11d]==0);
#ifdef AK820_MAC_PC
    for (unsigned mac=0;mac<2;++mac) {
        ak820_mac_mode=mac; os_now=100; os_request(1,1,0,1);
        os_now=3100; layer_state=default_layer_state=1;
        ak820_update_indicators();
        assert(ak820_led_dma[0x13f]==(mac?255:0));
        assert(ak820_led_dma[0x13d]==0 && ak820_led_dma[0x13c]==(mac?255:0));
    }
#endif
    for (unsigned sleeping=0;sleeping<2;++sleeping) {
        os_now=5000; os_request(1,2,0,2);
        layer_state=default_layer_state=2; KB_USB_SetReport=2;
        caps_word_led_active = true;
        if(sleeping) USB_SleepStatus=2; else D0UsbConfig=0;
        ak820_update_indicators();
        assert(ak820_led_dma[0x11c]==0 && ak820_led_dma[0x11d]==0);
        assert(ak820_led_dma[0x13c]==0 && ak820_led_dma[0x13d]==0 && ak820_led_dma[0x13f]==0);
        USB_SleepStatus=0; D0UsbConfig=1;
    }
    caps_word_led_active = false;
    /* Long unattended gaps and 32-bit wrap cannot resurrect a stale override. */
    os_now=0xfffffff0; os_request(1,1,0,1);
    os_now=0x00000ba7; os_request(0,0,0,1);
    os_now=0x00000ba8; os_request(0,0,0,0);
    os_now=10; os_request(1,2,0,2); os_now=65546; os_request(0,0,0,0);
    for (unsigned phase=0;phase<256;++phase) {
        os_now=phase*16; os_request(1,3,0,3);
        uint8_t expected=phase<128?phase*2:(255-phase)*2;
        assert(ak820_os_indicator_value(73)==expected);
    }
    puts("PASS: OS indicator production USB path, exact wire replies, malformed requests, no NVM, lease, IRQ restoration, lifecycle cancellation and DMA ownership");
}

#ifdef AK820_COMPACT_GUI_LOCK
static void test_gui_lock_w_channel(void) {
    fresh(); configure(); gui_active=false; layer_state=default_layer_state=1;
    KB_USB_SetReport=0; os_now=0;
    memset(ak820_led_dma,0,sizeof(ak820_led_dma)); ak820_update_indicators();
    assert(ak820_led_dma[0x13d]==0); /* default off */
    gui_active=true;
    for (unsigned t=0;t<=2000;t+=250) {
        os_now=t; ak820_update_indicators();
        uint16_t phase=(uint16_t)(t%2000);
        uint8_t expected=ak820_breathing_wave((uint8_t)(192u+((phase<<4)/125u)));
        assert(ak820_led_dma[0x13d]==expected);
        assert(ak820_led_dma[0x13c]==255);
        assert(ak820_led_dma[0x11c]==0 && ak820_led_dma[0x11d]==0);
    }
    layer_state=2; os_now=2100; ak820_update_indicators(); assert(ak820_led_dma[0x13d]==255);
    layer_state=default_layer_state=1; gui_active=false; os_now=2200; ak820_update_indicators(); assert(ak820_led_dma[0x13d]==0);
    gui_active=true; os_now=2300; ak820_update_indicators();
    USB_SleepStatus=2; ak820_update_indicators(); assert(ak820_led_dma[0x13d]==0);
    USB_SleepStatus=0; D0UsbConfig=0; ak820_update_indicators(); assert(ak820_led_dma[0x13d]==0);
    D0UsbConfig=1; gui_active=false;
    puts("PASS: GUI-lock W host fixture: default off, 2s extracted-wave pulse, layer priority, Caps separation, suspend/unconfigured");
}
#endif
