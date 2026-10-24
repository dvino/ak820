static uint16_t t;
static void fresh(void) { reset();as_enabled=false;as_state=0;ak820_leader_cancel();macro_available=false;t=100;assign(0,QK_LEAD);assign(1,KC_1);assign(2,KC_A); }
static void press(unsigned id) {event(id,true,t+=10);}
static void release(unsigned id) {event(id,false,t+=1);}
static void tap(unsigned id) {press(id);release(id);}
int main(void) {
 for(unsigned i=0;i<16;i++) {fresh();assign(1,i<10?KC_1+i:KC_A+i-10);tap(0);press(1);assert(leader_pending==i&&!leader_waiting);assert(!is_key_pressed(keyboard_report,i<10?KC_1+i:KC_A+i-10));release(1);tick(t+=1);assert(leader_pending==NONE);}
 fresh();press(2);tap(0);release(2);assert(!is_key_pressed(keyboard_report,KC_A)&&leader_waiting);tap(1);assert(!leader_waiting);
 fresh();tap(0);t+=300;press(2);assert(!leader_waiting&&is_key_pressed(keyboard_report,KC_A));release(2);
 fresh();t=65520;tap(0);t=20;press(1);assert(leader_pending==0);release(1);
 fresh();tap(0);assign(1,KC_ESC);tap(1);assert(!leader_waiting&&leader_pending==NONE&&!is_key_pressed(keyboard_report,KC_ESC));
 fresh();press(0);press(1);clear_keyboard();release(0);release(1);assert(!leader_waiting&&leader_pending==NONE);tap(2);assert(!is_key_pressed(keyboard_report,KC_A));
 fresh();assign(3,OSM(MOD_LSFT));tap(3);tap(0);tap(1);assert(ak820_oneshot_mods==2);press(2);assert(!ak820_oneshot_mods&&ak820_oneshot_consumed==2);release(2);assert(!get_mods());
 fresh();vial_keycode_down(QK_LEAD);vial_keycode_up(QK_LEAD);assert(!leader_waiting);enc[0][0]=QK_LEAD;encoder(false,true,t+=10);encoder(false,false,t+=1);assert(!leader_waiting);
 fresh();tap(0);assign(1,MT(MOD_LCTL,KC_B));press(1);assert(!leader_waiting);release(1);assert(!get_mods());
 fresh();caps_word_on();tap(0);tap(1);assert(is_caps_word_on());
 fresh();press(0);event(0,true,t+=100);assert(leader_started==110);release(0);tap(0);assert(leader_started==221);
 fresh();tap(0);vial_unlock_in_progress=true;clear_keyboard();tick(t+=10);assert(!leader_waiting&&leader_pending==NONE);vial_unlock_in_progress=false;
 fresh();fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();press(2);assert(!is_key_pressed(keyboard_report,KC_A));press(0);assert(is_key_pressed(keyboard_report,KC_A));press(1);assert(leader_pending==0);release(2);assert(!is_key_pressed(keyboard_report,KC_A));release(1);release(0);
 fresh();tap(0);tap(1);assign(3,QK_LEAD);tap(3);assign(4,KC_F);tap(4);assert(leader_pending==0&&!leader_waiting);tick(t+=1);assert(leader_pending==NONE);
 fresh();uint8_t body[]={1,2,KC_Z,1,3,KC_Z};macro_load(body,sizeof(body));assign(3,OSM(MOD_LSFT));tap(3);tap(0);tap(1);assert(ak820_oneshot_mods==2);tick(t+=1);assert(ak820_oneshot_mods==2);bool sent=false;for(unsigned i=0;i<log_count;i++)if(log_reports[i][2]==KC_Z&&log_reports[i][0]==2)sent=true;assert(sent);press(2);release(2);assert(!get_mods());
 fresh();tap(2);assert(get_last_keycode()==KC_A);tap(0);tap(1);assert(get_last_keycode()==KC_A);
 fresh();tap(0);assign(1,KC_LCTL);press(1);assert(!leader_waiting&&get_mods()==1);release(1);assert(!get_mods());
 fresh();tap(0);press(1);assign(1,KC_A);release(1);tick(t+=1);assert(!is_key_pressed(keyboard_report,KC_A));
 puts("Leader host cases passed");return 0;
}
