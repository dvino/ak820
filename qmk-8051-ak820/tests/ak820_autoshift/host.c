static bool has(uint8_t code) {for(unsigned i=0;i<6;i++)if(keyboard_report->keys[i]==code)return true;return false;}
static void fresh(void) {reset();ak820_autoshift_configure(1);ak820_caps_word_configure(0);assign(0,KC_A);assign(1,KC_B);assign(2,KC_LSFT);assign(3,KC_LCTL);}
int main(void) {
 /* All accepted basic keys, exact threshold and rollover. */
 for(unsigned code=KC_A;code<=KC_NONUS_BACKSLASH;code++) {
  bool eligible=(code<=KC_0)||(code>=KC_MINUS&&code<=KC_SLASH)||code==KC_NONUS_BACKSLASH;
  if(!eligible)continue;
  fresh();assign(0,code);event(0,true,100);assert(!has(code));tick(274);assert(!has(code));tick(275);assert(has(code)&&get_mods()==2);event(0,false,276);assert(!has(code)&&!get_mods());
 }
 fresh();event(0,true,65500);tick(138);assert(!has(KC_A));tick(139);assert(has(KC_A)&&get_mods()==2);event(0,false,140);assert(!has(KC_A)&&!get_mods());
 fresh();event(0,true,100);event(0,false,274);assert(!has(KC_A)&&!get_mods());assert(log_count>=2);assert(log_reports[log_count-2][2]==KC_A&&log_reports[log_count-2][0]==0);
 fresh();event(0,true,100);event(0,false,275);assert(!has(KC_A)&&!get_mods());assert(log_reports[log_count-3][2]==KC_A&&log_reports[log_count-3][0]==2);
 /* Interrupted pending press is sent first and both physical releases match. */
 fresh();event(0,true,100);event(1,true,120);assert(has(KC_A)&&has(KC_B)&&!get_mods());assert(log_reports[0][2]==KC_A&&log_reports[0][3]==0);event(0,false,130);assert(!has(KC_A)&&has(KC_B));event(1,false,140);
 /* Live remapping cannot change the deferred press or its release. */
 fresh();event(0,true,100);assign(0,KC_C);tick(275);assert(has(KC_A)&&!has(KC_C));event(0,false,300);assert(!has(KC_A)&&!get_mods());event(0,true,400);tick(575);assert(has(KC_C));event(0,false,600);
 /* Ownership survives both real Shift release orders. */
 for(unsigned first=0;first<2;first++) {
  fresh();event(0,true,100);tick(275);event(2,true,280);assert(get_mods()==2);
  event(first?0:2,false,290);assert(get_mods()==2);event(first?2:0,false,300);assert(!get_mods());
 }
 fresh();event(3,true,100);event(0,true,110);assert(has(KC_A)&&get_mods()==1&&!as_state);event(0,false,120);event(3,false,130);
 /* Encoded modifier owners bypass the delay without losing their owner. */
 fresh();assign(4,LCTL(KC_C));event(4,true,100);event(0,true,110);assert(has(KC_A)&&get_weak_mods()==1&&!as_state);event(0,false,120);assert(get_weak_mods()==1);event(4,false,130);assert(!get_weak_mods());
 /* Queued OSM bypasses delay and is consumed through its original source. */
 fresh();assign(4,OSM(MOD_LSFT));event(4,true,100);event(4,false,110);event(0,true,120);assert(has(KC_A)&&get_mods()==2&&!as_state);event(0,false,130);assert(!get_mods());
 /* CapsWord remains active, with weak Shift surviving emission. */
 fresh();caps_word_on();event(0,true,100);event(0,false,130);assert(is_caps_word_on());assert(log_reports[log_count-2][0]==2);caps_word_off();
 /* Repeat captures owned auto Shift; AltRepeat resolves bracket opposite. */
 fresh();assign(4,QK_REPEAT_KEY);event(0,true,100);tick(275);event(0,false,280);event(4,true,300);assert(has(KC_A)&&(get_mods()|get_weak_mods())==2);event(4,false,310);assert(!has(KC_A)&&!(get_mods()|get_weak_mods()));
 fresh();assign(0,KC_LBRC);assign(4,QK_ALT_REPEAT_KEY);event(0,true,100);tick(275);event(0,false,280);event(4,true,300);assert(has(KC_RBRC)&&(get_mods()|get_weak_mods())==2);event(4,false,310);
 /* Combo input fallback and combo output bypass AS. */
 fresh();fixture_combos[0].input[0]=KC_A;fixture_combos[0].input[1]=KC_B;fixture_combos[0].output=KC_C;ak820_combo_reload();event(0,true,100);tick(140);assert(has(KC_A)&&!as_state);event(0,false,150);
 fresh();fixture_combos[0].input[0]=KC_A;fixture_combos[0].input[1]=KC_B;fixture_combos[0].output=KC_C;ak820_combo_reload();event(0,true,100);event(1,true,120);assert(has(KC_C)&&!as_state);event(0,false,130);event(1,false,140);assert(!has(KC_C));
 /* Dual-role and SpaceCadet taps stay in the existing synthetic path. */
 fresh();assign(0,MT(MOD_LCTL,KC_A));event(0,true,100);event(0,false,120);assert(!as_state&&!get_mods()&&!has(KC_A));
 fresh();assign(0,SC_LSPO);event(0,true,100);event(0,false,120);assert(!as_state&&!get_mods()&&!has(KC_9));
 /* Encoder and macro generated basics never acquire an AS source. */
 fresh();enc[0][0]=KC_A;encoder(false,true,100);assert(has(KC_A)&&!as_state);encoder(false,false,110);
 fresh();vial_keycode_down(KC_A);assert(has(KC_A)&&!as_state);vial_keycode_up(KC_A);
 /* Cancellation never revives pending or emitted reports on release/tick. */
 for(unsigned shifted=0;shifted<2;shifted++) {
  fresh();event(0,true,100);if(shifted)tick(275);clear_keyboard();tick(400);assert(!has(KC_A)&&!get_mods()&&!as_state);event(0,false,410);assert(!has(KC_A)&&!as_state);event(0,true,500);tick(675);assert(has(KC_A));event(0,false,680);
 }
 /* Controls disable new admissions without losing an already-held release. */
 fresh();assign(4,QK_AUTO_SHIFT_OFF);assign(5,QK_AUTO_SHIFT_ON);assign(6,QK_AUTO_SHIFT_TOGGLE);event(0,true,100);event(4,true,110);assert(has(KC_A)&&!(as_flags & 1));event(4,false,120);event(0,false,130);event(1,true,140);assert(has(KC_B)&&!as_state);event(1,false,150);event(5,true,160);event(5,false,170);event(0,true,180);assert(as_state==1&&!has(KC_A));event(0,false,190);event(6,true,200);event(6,false,210);assert(!(as_flags & 1));
 /* Every category mask independently controls new admissions. */
 for(unsigned mask=0;mask<8;mask++) {
  uint8_t flags=1|((mask&1)?4:0)|((mask&2)?8:0)|((mask&4)?16:0);
  const uint8_t codes[]={KC_A,KC_1,KC_MINUS,KC_NONUS_BACKSLASH};
  for(unsigned j=0;j<4;j++) {
   fresh();ak820_autoshift_configure(flags);assign(0,codes[j]);event(0,true,100);
   bool disabled=flags&(j==0?16:j==1?8:4);
   assert((as_state==1)==!disabled);assert(has(codes[j])==disabled);event(0,false,110);
  }
  fresh();ak820_autoshift_configure(flags);assign(4,QK_AUTO_SHIFT_OFF);assign(5,QK_AUTO_SHIFT_ON);
  event(4,true,100);event(4,false,110);assert(as_flags==(flags&~1));
  event(5,true,120);event(5,false,130);assert(as_flags==flags);
 }
 /* Configuration changes preserve pending and shifted release owners. */
 for(unsigned shifted=0;shifted<2;shifted++) {
  fresh();event(0,true,100);if(shifted)tick(275);ak820_autoshift_configure(28);
  event(0,false,300);assert(!has(KC_A)&&!get_mods()&&!as_state);
  event(1,true,310);assert(has(KC_B)&&!as_state);event(1,false,320);
 }
 /* RU adds Cyrillic punctuation positions; EN punctuation still ends words. */
 const uint8_t ru_letters[]={KC_LBRC,KC_RBRC,KC_SCLN,KC_QUOT,KC_COMM,KC_DOT,KC_GRV};
 for(unsigned lang=0;lang<2;lang++) {
  for(unsigned j=0;j<sizeof(ru_letters);j++) {
   fresh();ak820_autoshift_configure(0);ak820_caps_word_configure(lang);caps_word_on();assign(0,ru_letters[j]);
   event(0,true,100);assert(is_caps_word_on()==lang);assert((get_weak_mods()==2)==lang);event(0,false,110);caps_word_off();
  }
  const uint16_t keep[]={KC_A,KC_1,KC_BSPC,KC_DEL,KC_UNDS,KC_MINS};
  for(unsigned j=0;j<sizeof(keep)/sizeof(*keep);j++) {
   fresh();ak820_autoshift_configure(0);ak820_caps_word_configure(lang);caps_word_on();assign(0,keep[j]);event(0,true,100);assert(is_caps_word_on());event(0,false,110);caps_word_off();
  }
 }
 /* Physical selectors change language and end a word only on a change. */
 fresh();ak820_autoshift_configure(0);assign(4,AK820_CW_LANG_RU);assign(5,AK820_CW_LANG_EN);assign(6,AK820_CW_LANG_TOGGLE);
 caps_word_on();event(0,true,100);assert(get_weak_mods()==2);event(4,true,110);assert(!is_caps_word_on()&&!get_weak_mods());event(4,false,120);event(0,false,130);
 caps_word_on();event(4,true,140);assert(is_caps_word_on());event(4,false,150);
 event(6,true,160);assert(!is_caps_word_on());event(6,false,170);assert(!caps_word_ru);
 /* Encoder and Vial macro selectors never change language or stop a word. */
 caps_word_on();enc[0][0]=AK820_CW_LANG_RU;encoder(false,true,200);encoder(false,false,210);assert(!caps_word_ru&&is_caps_word_on());
 vial_keycode_down(AK820_CW_LANG_RU);vial_keycode_up(AK820_CW_LANG_RU);assert(!caps_word_ru&&is_caps_word_on());
 /* A macro primitive borrowing a physical position is still excluded. */
 keyrecord_t generated={0};generated.event.pressed=true;ak820_macro_primitive=true;
 assert(!process_caps_word(AK820_CW_LANG_RU,&generated));ak820_macro_primitive=false;assert(!caps_word_ru&&is_caps_word_on());
 /* Configuration preserves the existing idle deadline and timer behavior. */
 caps_word_off();now=1000;caps_word_on();uint16_t deadline=idle_timer;ak820_caps_word_configure(0);assert(idle_timer==deadline);now=deadline;caps_word_task();assert(!is_caps_word_on());
 puts("Auto Shift production host cases passed");return 0;
}
