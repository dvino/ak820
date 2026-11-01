static uint16_t t;
static void fresh(void) { reset();as_flags=0;as_state=0;ak820_leader_cancel();macro_available=false;t=100;assign(0,QK_LEAD);assign(1,KC_1);assign(2,KC_A); }
static void press(unsigned id) {event(id,true,t+=10);}
static void release(unsigned id) {event(id,false,t+=1);}
static void tap(unsigned id) {press(id);release(id);}
static bool leader_event(unsigned row, unsigned col, bool down) {
 keyrecord_t r={0};r.event.type=KEY_EVENT;r.event.key.row=row;r.event.key.col=col;r.event.pressed=down;r.event.time=100;r.keycode=QK_LEAD;
 return ak820_leader_process(&r);
}
static bool direct_leader(uint16_t code, bool down) {
 keyrecord_t r={0};r.event.type=KEY_EVENT;r.event.key.row=0;r.event.key.col=1;r.event.pressed=down;r.event.time=t;r.keycode=code;
 return ak820_leader_process(&r);
}
int main(void) {
 /* Exhaustively compare the production event path with the original inclusive range. */
 for(unsigned code=0;code<=UINT16_MAX;code++) {
  fresh();assert(!leader_event(0,0,true));assert(!leader_event(0,0,false));
  bool expected=!(code>=KC_A&&code<=KC_EXSEL);
  if(code==QK_LEAD) expected=false; /* The Leader key itself starts the sequence. */
  bool actual=direct_leader((uint16_t)code,true);
  if(actual!=expected) {fprintf(stderr,"predicate mismatch code=%04x actual=%d expected=%d\\n",code,actual,expected);abort();}
  assert(leader_waiting==(code==QK_LEAD));
  assert(direct_leader((uint16_t)code,false)==expected);
 }
 /* Boundary admission also checks selector queueing and suppression of both edges. */
 const uint16_t boundaries[]={0x0003,0x0004,0x00a4,0x00a5,0x0104,0xffff};
 const uint8_t slots[]={NONE,10,NONE,NONE,NONE,NONE};
 for(unsigned i=0;i<sizeof(boundaries)/sizeof(boundaries[0]);i++) {
  fresh();assert(!leader_event(0,0,true));assert(!leader_event(0,0,false));
  bool expected=!(boundaries[i]>=KC_A&&boundaries[i]<=KC_EXSEL);
  assert(direct_leader(boundaries[i],true)==expected);
  if(leader_waiting||leader_pending!=slots[i]) {fprintf(stderr,"boundary mismatch code=%04x wait=%d pending=%u\\n",boundaries[i],leader_waiting,leader_pending);abort();}
  assert(direct_leader(boundaries[i],false)==expected);
 }
 /* All sources at once cover both sides of each bitmap boundary and the last bit. */
 fresh();
 for(unsigned id=0;id<LEADER_SOURCES;id++) {
  assert(!leader_event(id/MATRIX_COLS,id%MATRIX_COLS,true));
  assert(!leader_event(id/MATRIX_COLS,id%MATRIX_COLS,true));
 }
 assert(leader_event(MATRIX_ROWS,0,true));assert(leader_event(0,MATRIX_COLS,true));
 for(unsigned id=LEADER_SOURCES;id-- > 0;) {
  assert(!leader_event(id/MATRIX_COLS,id%MATRIX_COLS,false));
  assert(leader_event(id/MATRIX_COLS,id%MATRIX_COLS,false));
 }
 for(unsigned unlock=0;unlock<2;unlock++) {
  fresh();
  for(unsigned id=0;id<LEADER_SOURCES;id++) assert(!leader_event(id/MATRIX_COLS,id%MATRIX_COLS,true));
  if(unlock) {vial_unlock_in_progress=true;ak820_leader_task(100);vial_unlock_in_progress=false;} else ak820_leader_cancel();
  assert(!leader_waiting&&leader_pending==NONE);
  for(unsigned id=0;id<LEADER_SOURCES;id++) assert(leader_event(id/MATRIX_COLS,id%MATRIX_COLS,false));
 }
 /* Exercise the actual last valid instant and first expired instant, including 1 ms. */
 fresh();event(0,true,100);event(0,false,100);event(1,true,100+AK820_LEADER_TIMEOUT-1);assert(leader_pending==0&&!leader_waiting);event(1,false,100+AK820_LEADER_TIMEOUT-1);
 fresh();event(0,true,100);event(0,false,100);event(1,true,100+AK820_LEADER_TIMEOUT);assert(!leader_waiting&&is_key_pressed(keyboard_report,KC_1));event(1,false,100+AK820_LEADER_TIMEOUT);
 /* A buffered Combo input resolves before Leader; cancellation prevents admission. */
 for(unsigned shift=0;shift<2;shift++) for(unsigned cancel=0;cancel<2;cancel++) {
  fresh();ak820_autoshift_configure(shift);fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();
  event(2,true,100);assert(!log_count);cancel_in_record=cancel;event(0,true,110);
  assert(leader_waiting==!cancel);
  if(cancel) assert(!log_count&&!as_state&&first==NONE);
  else {assert(log_count&&log_reports[0][2]==KC_A&&!log_reports[0][0]);assert(is_key_pressed(keyboard_report,KC_A));}
  event(0,false,111);event(2,false,112);assert(!is_key_pressed(keyboard_report,KC_A)&&!as_state);
 }
 if (AK820_LEADER_TIMEOUT == 1) { puts("Leader endpoint cases passed"); return 0; }
 for(unsigned i=0;i<16;i++) {fresh();assign(1,i<10?KC_1+i:KC_A+i-10);tap(0);press(1);assert(leader_pending==i&&!leader_waiting);assert(!is_key_pressed(keyboard_report,i<10?KC_1+i:KC_A+i-10));release(1);tick(t+=1);assert(leader_pending==NONE);}
 fresh();press(2);tap(0);release(2);assert(!is_key_pressed(keyboard_report,KC_A)&&leader_waiting);tap(1);assert(!leader_waiting);
 fresh();tap(0);t+=AK820_LEADER_TIMEOUT;press(2);assert(!leader_waiting&&is_key_pressed(keyboard_report,KC_A));release(2);
 fresh();tap(0);tick(leader_started+AK820_LEADER_TIMEOUT-1);assert(leader_waiting);tick(leader_started+AK820_LEADER_TIMEOUT);assert(!leader_waiting);
 fresh();tap(0);t=leader_started+AK820_LEADER_TIMEOUT-11;press(1);assert(leader_pending==0);release(1);
 fresh();tap(0);t=leader_started+AK820_LEADER_TIMEOUT-10;press(1);assert(!leader_waiting&&is_key_pressed(keyboard_report,KC_1));release(1);
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
 fresh();ak820_autoshift_configure(1);fixture_combos[0]=(vial_combo_entry_t){{KC_A,KC_B,0,0},KC_C};ak820_combo_reload();press(2);press(0);assert(is_key_pressed(keyboard_report,KC_A)&&!get_mods()&&leader_waiting);release(2);assert(!is_key_pressed(keyboard_report,KC_A));release(0);tap(1);assert(leader_pending==0);
 fresh();tap(0);tap(1);assign(3,QK_LEAD);tap(3);assign(4,KC_F);tap(4);assert(leader_pending==0&&!leader_waiting);tick(t+=1);assert(leader_pending==NONE);
 fresh();uint8_t body[]={1,2,KC_Z,1,3,KC_Z};macro_load(body,sizeof(body));assign(3,OSM(MOD_LSFT));tap(3);tap(0);tap(1);assert(ak820_oneshot_mods==2);tick(t+=1);assert(ak820_oneshot_mods==2);bool sent=false;for(unsigned i=0;i<log_count;i++)if(log_reports[i][2]==KC_Z&&log_reports[i][0]==2)sent=true;assert(sent);press(2);release(2);assert(!get_mods());
 fresh();tap(2);assert(get_last_keycode()==KC_A);tap(0);tap(1);assert(get_last_keycode()==KC_A);
 fresh();tap(0);assign(1,KC_LCTL);press(1);assert(!leader_waiting&&get_mods()==1);release(1);assert(!get_mods());
 fresh();tap(0);press(1);assign(1,KC_A);release(1);tick(t+=1);assert(!is_key_pressed(keyboard_report,KC_A));
 puts("Leader host cases passed");return 0;
}
