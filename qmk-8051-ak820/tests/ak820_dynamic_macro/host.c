static bool has(uint8_t code) { return is_key_pressed(keyboard_report,code); }
static uint16_t t;
static void fresh(void) {
 reset();memset(dm_taps,0,sizeof(dm_taps));memset(dm_lengths,0,sizeof(dm_lengths));dm_record=dm_play=dm_down=0;dm_busy=false;as_enabled=false;as_state=0;t=100;
 assign(0,KC_A);assign(1,KC_B);assign(2,KC_LSFT);assign(3,KC_LCTL);
}
static void ctl(uint16_t code) {assign(4,code);event(4,true,t+=20);event(4,false,t+=1);}
static void tap(uint8_t id) {event(id,true,t+=20);event(id,false,t+=20);}
static void step(void) {tick(t+=20);}
static void recorded(void) {ctl(DM_REC1);tap(0);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].code==KC_A);}
int main(void) {
 fresh();recorded();ctl(DM_PLY1);step();assert(has(KC_A));step();assert(!has(KC_A));step();assert(!dm_play);
 /* Rolling typing preserves press order despite reversed release order. */
 fresh();ctl(DM_REC1);event(0,true,t+=20);event(1,true,t+=20);event(1,false,t+=20);event(0,false,t+=20);ctl(DM_RSTP);
 assert(dm_lengths[0]==2&&dm_taps[0].code==KC_A&&dm_taps[1].code==KC_B);
 ctl(DM_PLY1);step();assert(has(KC_A)&&!has(KC_B));step();step();assert(has(KC_B)&&!has(KC_A));step();step();assert(!dm_play);
 /* Stop drops incomplete taps, retains completed followers, late release inert. */
 fresh();ctl(DM_REC1);event(0,true,t+=20);tap(1);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].code==KC_B);event(0,false,t+=20);assert(dm_lengths[0]==1);
 /* A pre-held usage cannot complete a new unrelated slot. */
 fresh();event(0,true,t+=20);ctl(DM_REC1);event(0,false,t+=20);ctl(DM_RSTP);assert(!dm_lengths[0]);
 /* Fixed capacity, overwrite only selected slot, both independent slots. */
 fresh();ctl(DM_REC1);for(unsigned i=0;i<20;i++)tap(0);ctl(DM_RSTP);assert(dm_lengths[0]==16);
 ctl(DM_REC2);tap(1);ctl(DM_RSTP);assert(dm_lengths[1]==1&&dm_taps[16].code==KC_B&&dm_lengths[0]==16);
 ctl(DM_REC1);tap(1);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].code==KC_B&&dm_lengths[1]==1);
 /* Effective OSM, encoded modifiers, Caps Word and Auto Shift. */
 fresh();ctl(DM_REC1);assign(5,OSM(MOD_LSFT));tap(5);tap(0);ctl(DM_RSTP);assert(dm_taps[0].mods==2);
 ctl(DM_PLY1);step();assert(has(KC_A)&&get_mods()==2);step();assert(!get_mods());step();
 fresh();ctl(DM_REC1);assign(5,LCTL(KC_C));tap(5);ctl(DM_RSTP);assert(dm_taps[0].code==KC_C&&dm_taps[0].mods==1);
 fresh();ctl(DM_REC1);caps_word_on();tap(0);caps_word_off();ctl(DM_RSTP);assert(dm_taps[0].mods==2);
 fresh();as_enabled=true;ctl(DM_REC1);event(0,true,t+=20);tick(t+=175);event(0,false,t+=20);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].mods==2);
 /* Generated Repeat, encoder, Vial macro and unsupported usage excluded. */
 fresh();ctl(DM_REC1);tap(0);assign(5,QK_REPEAT_KEY);tap(5);enc[0][0]=KC_B;encoder(false,true,t+=20);encoder(false,false,t+=20);vial_keycode_down(KC_C);vial_keycode_up(KC_C);assign(5,KC_EXSEL);tap(5);ctl(DM_RSTP);assert(dm_lengths[0]==1);
 /* Tap-hold/Combo outputs are physical handlers; synthetic Grave Escape is excluded. */
 fresh();ctl(DM_REC1);assign(5,MT(MOD_LCTL,KC_C));tap(5);assign(5,QK_GRAVE_ESCAPE);tap(5);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].code==KC_C);
 fresh();fixture_combos[0].input[0]=KC_A;fixture_combos[0].input[1]=KC_B;fixture_combos[0].output=KC_C;ak820_combo_reload();ctl(DM_REC1);event(0,true,t+=20);event(1,true,t+=20);event(0,false,t+=1);event(1,false,t+=1);ctl(DM_RSTP);assert(dm_lengths[0]==1&&dm_taps[0].code==KC_C);
 /* Vial-generated macro controls cannot start recording or playback. */
 fresh();recorded();vial_keycode_down(DM_PLY1);vial_keycode_up(DM_PLY1);assert(!dm_play);vial_keycode_down(DM_REC2);vial_keycode_up(DM_REC2);assert(!dm_record);
 /* Same usage already held: skip playback, balance borrowed ref, never release it. */
 fresh();recorded();event(0,true,t+=20);ctl(DM_PLY1);step();assert(has(KC_A)&&!dm_down);step();assert(!dm_play&&has(KC_A));event(0,false,t+=20);assert(!has(KC_A));
 /* Physical owner arrives while replay owns A: release replay preserves A. */
 fresh();recorded();ctl(DM_PLY1);step();event(0,true,t+=1);step();assert(has(KC_A)&&!dm_down);event(0,false,t+=1);assert(!has(KC_A));step();
 /* Nested Vial primitive events cannot acquire playback ownership. */
 fresh();recorded();ctl(DM_PLY1);ak820_macro_primitive=true;step();assert(!dm_down&&dm_play);ak820_macro_primitive=false;step();assert(has(KC_A));step();assert(!has(KC_A));step();assert(!dm_play);
 /* A due release inside a primitive also waits, preserving its key/Shift refs. */
 fresh();ctl(DM_REC1);event(2,true,t+=20);tap(0);event(2,false,t+=1);ctl(DM_RSTP);ctl(DM_PLY1);step();assert(has(KC_A)&&get_mods()==2);ak820_macro_primitive=true;step();assert(has(KC_A)&&get_mods()==2);ak820_macro_primitive=false;step();assert(!has(KC_A)&&!get_mods());step();assert(!dm_play);
 /* Both modifier ownership release orders preserve physical Shift. */
 for(unsigned first=0;first<2;first++) {
  fresh();ctl(DM_REC1);event(2,true,t+=20);tap(0);event(2,false,t+=20);ctl(DM_RSTP);ctl(DM_PLY1);step();event(2,true,t+=1);
  if(first){event(2,false,t+=1);assert(get_mods()==2);step();assert(!get_mods());}
  else {step();assert(get_mods()==2);event(2,false,t+=1);assert(!get_mods());}step();
 }
 /* Busy down and busy release pause; no later tap can overwrite latest release. */
 fresh();recorded();ctl(DM_PLY1);dm_busy=true;step();assert(!has(KC_A)&&dm_play);dm_busy=false;step();assert(has(KC_A));dm_busy=true;step();assert(has(KC_A));dm_busy=false;step();assert(!has(KC_A)&&dm_play);dm_busy=true;step();assert(dm_play);dm_busy=false;step();assert(!dm_play);
 /* Clear cancels live replay and recording without revival; stored taps survive. */
 fresh();ctl(DM_REC1);tap(0);tap(1);ctl(DM_RSTP);ctl(DM_PLY1);step();assert(has(KC_A));clear_keyboard();step();assert(!has(KC_A)&&!has(KC_B)&&!dm_play&&!get_mods()&&dm_lengths[0]==2);
 fresh();ctl(DM_REC1);tap(1);event(0,true,t+=20);clear_keyboard();event(0,false,t+=20);step();assert(!dm_record&&dm_lengths[0]==1&&dm_taps[0].code==KC_B&&!has(KC_A));
 /* Controls during replay are consumed and cannot recurse or overwrite. */
 fresh();recorded();ctl(DM_PLY1);step();ctl(DM_REC1);ctl(DM_PLY2);ctl(DM_RSTP);while(dm_play)step();assert(dm_lengths[0]==1&&!dm_record);
 /* A rollover-hidden physical usage remains owned when replay skips it. */
 fresh();recorded();for(unsigned i=0;i<7;i++){assign(10+i,KC_A+i);event(10+i,true,t+=20);}ctl(DM_PLY1);step();step();assert(!dm_play);for(unsigned i=1;i<7;i++)event(10+i,false,t+=20);assert(has(KC_A));event(10,false,t+=20);assert(!has(KC_A));
 /* NKRO duplicate balance follows the same owner reference contract. */
 fresh();keymap_config.nkro=true;recorded();event(0,true,t+=20);ctl(DM_PLY1);step();step();assert(has(KC_A));event(0,false,t+=20);assert(!has(KC_A));keymap_config.nkro=false;
 /* Timer wrap still advances once, no catch-up burst. */
 fresh();recorded();now=65530;t=65530;ak820_dynamic_macro_process(DM_PLY1,true);tick(3);assert(!has(KC_A));tick(4);assert(has(KC_A));tick(14);assert(!has(KC_A));tick(24);assert(!dm_play);
 puts("Dynamic Macro production host cases passed");return 0;
}
