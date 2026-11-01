static bool has(uint8_t code) { return is_key_pressed(keyboard_report,code); }
static void fresh(void) {
 reset();ak820_autoshift_configure(1);ak820_caps_word_configure(0);
 assign(0,KC_A);assign(1,KC_B);
 fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();
}
int main(void) {
 const unsigned combo=TEST_COMBO_TERM, shift=TEST_SHIFT_TERM;
 /* Releases just before and at each deadline, without intervening scans. */
 const unsigned points[]={combo-1,combo,shift-1,shift};
 for(unsigned i=0;i<4;i++) {
  fresh();event(0,true,100);event(0,false,100+points[i]);
  bool found=false, released=false;
  for(unsigned j=0;j<log_count;j++) {
   bool a=false;for(unsigned k=2;k<8;k++)if(log_reports[j][k]==KC_A)a=true;
   if(a) { assert(log_reports[j][0]==0);found=true; }
   else if(found) released=true;
  }
  assert(found&&released&&!has(KC_A)&&!get_mods()&&!as_state);
 }
 /* A failed candidate is emitted unshifted at the Combo deadline. */
 fresh();event(0,true,100);tick(100+combo-1);assert(!has(KC_A)&&!as_state);
 tick(100+combo);assert(has(KC_A)&&!as_state&&!get_mods());
 tick(100+(combo>shift?combo:shift)+1);assert(has(KC_A)&&!get_mods());
 event(0,false,100+(combo>shift?combo:shift)+2);assert(!has(KC_A)&&!get_mods());
 /* The second input wins strictly before, but not at, the Combo deadline. */
 fresh();event(0,true,100);event(1,true,100+combo-1);
#ifdef AK820_COMBO_AUTOSHIFT
 assert(!has(KC_C)&&as_state==1);
#else
 assert(has(KC_C)&&!has(KC_A)&&!has(KC_B));
#endif
 event(0,false,100+combo);event(1,false,101+combo);assert(!has(KC_C));
 fresh();event(0,true,100);event(1,true,100+combo);assert(!has(KC_C));event(0,false,101+combo);event(1,false,102+combo);
 bool a_seen=false,b_seen=false,a_up=false,b_up=false;uint8_t expected_mods=0;
 for(unsigned i=0;i<log_count;i++) {
  bool a=false,b=false,c=false;
  for(unsigned k=2;k<8;k++) { a|=log_reports[i][k]==KC_A;b|=log_reports[i][k]==KC_B;c|=log_reports[i][k]==KC_C; }
  assert(!c);
  if(a) { assert(log_reports[i][0]==expected_mods);a_seen=true; }
  if(b) { assert(log_reports[i][0]==0&&a_seen);b_seen=true; }
  if(a_seen&&!a)a_up=true;
  if(b_seen&&!b)b_up=true;
 }
 assert(a_seen&&b_seen&&a_up&&b_up&&!has(KC_A)&&!has(KC_B)&&!has(KC_C)&&!get_mods());
#ifdef AK820_COMBO_AUTOSHIFT
 /* Recognition owns the second position; either release ends output once. */
 for(unsigned order=0;order<2;order++) for(unsigned held=0;held<2;held++) for(unsigned scan=0;scan<2;scan++) {
  fresh();event(0,true,65500);event(1,true,65501);
  uint16_t end=(uint16_t)(65501+shift-(held?0:1));
  if(scan) tick(end);
  event(order?1:0,false,end);event(order?0:1,false,(uint16_t)(end+1));
  bool down=false,up=false;
  for(unsigned j=0;j<log_count;j++) {
   bool c=false;for(unsigned k=2;k<8;k++) c|=log_reports[j][k]==KC_C;
   if(c) {assert(log_reports[j][0]==(held?2:0));down=true;} else if(down) up=true;
  }
  assert(down&&up&&!active&&!as_state&&!has(KC_C)&&!get_mods());
 }
 /* Unrelated presses interrupt or time out the owner; the other input stays suppressed. */
 for(unsigned late=0;late<2;late++) {
  fresh();assign(2,KC_D);event(0,true,100);event(1,true,101);event(2,true,101+shift-(late?0:1));
  assert(has(KC_C)&&has(KC_D)&&get_mods()==(late?2:0));
  event(1,false,102+shift);assert(!has(KC_C)&&has(KC_D));event(0,false,103+shift);event(2,false,104+shift);
  assert(!active&&!as_state&&!get_mods());
 }
 /* A new owner can start after output release while the other input remains held. */
 fresh();assign(2,KC_D);event(0,true,100);event(1,true,101);event(1,false,102);event(2,true,103);
 assert(as_state==1&&active);event(0,false,104);assert(as_state==1&&!active);tick(103+shift);assert(has(KC_D)&&get_mods()==2);event(2,false,104+shift);assert(!as_state&&!get_mods());
 /* A clear during interruption must not admit the now-blocked interrupting key. */
 fresh();assign(2,KC_D);event(0,true,100);event(1,true,101);cancel_in_record=true;event(2,true,102);
 event(2,false,103);event(1,false,104);event(0,false,105);tick(106+shift);
 assert(!active&&!as_state&&!has(KC_C)&&!has(KC_D)&&!get_mods());
 /* Existing owner, disabled categories, modifiers and noneligible output fall back. */
 for(unsigned mode=0;mode<5;mode++) {
  fresh();assign(2,KC_D);assign(3,KC_LCTL);
  if(mode==0) event(2,true,90);
  if(mode==1) ak820_autoshift_configure(0);
  if(mode==2) ak820_autoshift_configure(17);
  if(mode==3) event(3,true,90);
  if(mode==4) {fixture_combos[0].output=KC_ENTER;ak820_combo_reload();}
  event(0,true,100);event(1,true,101);assert(has(mode==4?KC_ENTER:KC_C));
  event(1,false,102);event(0,false,103);assert(!active&&!has(KC_C)&&!has(KC_ENTER));
  if(mode==0) event(2,false,104);
  if(mode==3) event(3,false,104);
  assert(!as_state&&!get_mods());
 }
 /* Valid noneligible modified, modifier, consumer and Caps Word outputs stay immediate. */
 const uint16_t outputs[]={LCTL(KC_C),KC_LCTL,KC_AUDIO_MUTE,QK_CAPS_WORD_TOGGLE};
 for(unsigned i=0;i<4;i++) {
  fresh();fixture_combos[0].output=outputs[i];assert(ak820_combo_valid(&fixture_combos[0]));ak820_combo_reload();
  event(0,true,100);event(1,true,101);assert(!as_state);
  if(i==0)assert(has(KC_C)&&get_weak_mods()==1);
  if(i==1)assert(get_mods()==1);
  if(i==2)assert(consumers&&last_consumer);
  if(i==3)assert(is_caps_word_on());
  event(1,false,102);event(0,false,103);assert(!active&&!get_mods()&&!get_weak_mods());
  if(i==2)assert(!last_consumer);
  if(i==3)caps_word_off();
 }
 /* Queued One Shot and Caps Word see the actual successful output. */
 fresh();assign(2,OSM(MOD_LSFT));event(2,true,80);event(2,false,90);event(0,true,100);event(1,true,101);
 assert(has(KC_C)&&get_mods()==2&&!as_state);event(1,false,102);event(0,false,103);assert(!get_mods()&&!ak820_oneshot_mods&&!ak820_oneshot_consumed);
 fresh();caps_word_on();event(0,true,100);event(1,true,101);event(0,false,102);event(1,false,103);assert(is_caps_word_on());
 bool cw=false;for(unsigned i=0;i<log_count;i++)if(log_reports[i][0]==2)for(unsigned k=2;k<8;k++)if(log_reports[i][k]==KC_C)cw=true;
 assert(cw);caps_word_off();
 /* Repeat and Alternate Repeat remember the emitted shifted output. */
 for(unsigned alt=0;alt<2;alt++) {
  fresh();fixture_combos[0].output=KC_LBRC;ak820_combo_reload();assign(2,alt?QK_ALT_REPEAT_KEY:QK_REPEAT_KEY);
  event(0,true,100);event(1,true,101);tick(101+shift);event(1,false,102+shift);event(0,false,103+shift);
  event(2,true,104+shift);assert(has(alt?KC_RBRC:KC_LBRC)&&(get_mods()|get_weak_mods())==2);event(2,false,105+shift);
  assert(!(get_mods()|get_weak_mods()));
 }
 /* Synchronous cancellation during emission must not recreate either owner. */
 for(unsigned mode=0;mode<3;mode++) {
  fresh();if(mode==0)ak820_autoshift_configure(0);event(0,true,100);
  if(mode==0)cancel_in_record=true;
  event(1,true,101);
  if(mode!=0) {cancel_in_record=true;if(mode==1)event(1,false,102);else tick(101+shift);}
  event(1,false,103+shift);event(0,false,104+shift);tick(105+shift);
  assert(!active&&!as_state&&!has(KC_C)&&!get_mods());
 }
#endif
 /* Cancellation during failed-Combo flush cannot admit the blocked new source. */
 for(unsigned enabled=0;enabled<2;enabled++) {
  fresh();ak820_autoshift_configure(enabled);assign(2,KC_D);assign(3,KC_E);
  fixture_combos[1]=(vial_combo_entry_t){{KC_D,KC_E,0,0},KC_F};ak820_combo_reload();
  event(0,true,100);cancel_in_record=true;event(2,true,101);
  event(0,false,102);event(2,false,103);tick(100+combo+shift);
  assert(!active&&first==NONE&&!as_state&&!has(KC_A)&&!has(KC_D)&&!get_mods());
 }
 /* Encoder interruption must also stop when its flush cancels the keyboard. */
 for(unsigned enabled=0;enabled<2;enabled++) {
  fresh();ak820_autoshift_configure(enabled);enc[0][0]=KC_D;event(0,true,100);cancel_in_record=true;encoder(false,true,101);
  encoder(false,false,102);event(0,false,103);tick(104+combo+shift);
  assert(!active&&first==NONE&&!as_state&&!has(KC_A)&&!has(KC_D)&&!get_mods());
  for(unsigned i=0;i<log_count;i++)for(unsigned k=2;k<8;k++)assert(log_reports[i][k]!=KC_D);
 }
 /* Deadline flush cancels before tapping sees the simultaneous new press. */
 fresh();ak820_autoshift_configure(0);assign(2,KC_D);event(0,true,100);cancel_in_record=true;event(2,true,100+combo);
 event(2,true,101+combo);assert(!has(KC_D));event(2,false,102+combo);event(0,false,103+combo);tick(104+combo+shift);
 assert(!active&&first==NONE&&!as_state&&!has(KC_A)&&!has(KC_D)&&!get_mods());
 event(2,true,105+combo+shift);assert(has(KC_D));event(2,false,106+combo+shift);assert(!has(KC_D));
 /* A release discarded by a cancelling deadline flush must unblock its source. */
 fresh();ak820_autoshift_configure(0);assign(2,KC_D);event(2,true,90);assert(has(KC_D));event(0,true,100);
 cancel_in_record=true;event(2,false,100+combo);assert(!cancel_in_record&&!has(KC_D)&&!has(KC_A));
 unsigned after_clear=log_count;event(0,false,101+combo);tick(102+combo+shift);
 for(unsigned i=after_clear;i<log_count;i++)for(unsigned k=2;k<8;k++)assert(log_reports[i][k]!=KC_A&&log_reports[i][k]!=KC_D);
 event(2,true,103+combo+shift);assert(has(KC_D));event(2,false,104+combo+shift);assert(!has(KC_D)&&!active&&!as_state&&!get_mods());
 /* A control whose flush cancels must not change the session setting. */
 fresh();ak820_autoshift_configure(0);assign(2,QK_COMBO_OFF);event(0,true,100);cancel_in_record=true;event(2,true,101);
 event(2,false,102);event(0,false,103);assert(enabled&&!active&&!as_state);
#ifdef AK820_COMBO_AUTOSHIFT
 /* Combo control clears the pending output and held sources. */
 fresh();assign(2,QK_COMBO_OFF);event(0,true,100);event(1,true,101);event(2,true,102);
 event(2,false,103);event(1,false,104);event(0,false,105);tick(106+shift);
 assert(!active&&!as_state&&!has(KC_C)&&!get_mods());
 assign(2,QK_COMBO_ON);event(2,true,200+shift);event(2,false,201+shift);
 /* Shared clear cancels pending and shifted owners and blocks held sources. */
 for(unsigned held=0;held<2;held++) {
  fresh();event(0,true,100);event(1,true,101);if(held)tick(101+shift);
  clear_keyboard();tick(102+shift);event(1,false,103+shift);event(0,false,104+shift);
  assert(!active&&!as_state&&!has(KC_C)&&!get_mods());
 }
#endif
 puts("Combo/Auto Shift boundary cases passed");return 0;
}
