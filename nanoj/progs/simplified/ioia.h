void mode_position(){
	od_write(0x6060, 0x00, 0x1);
}

void mode_velocity(){
	od_write(0x6060, 0x00, 0x3);
}

void start(){
	od_write(0x6040, 0x00, 0x6);
	while ( (In.StatusWord & 0xEF) != 0x21) {
		yield();
	}
	od_write(0x6040, 0x00, 0x7);
	while ( (In.StatusWord & 0xEF) != 0x23) {
		yield();
	}
	od_write(0x6040, 0x00, 0xF);
	while ( (In.StatusWord & 0xEF) != 0x27) {
		yield();
	}
}

void stop(){
	od_write(0x6040, 0x00, 0x0);
	od_write(0x2300, 0x00, 0x0);
}

void target(U32 param){
	od_write(0x607A, 0x00, param);
	od_write(0x6040, 0x00, 0x7F);
	while ( (In.StatusWord) != 0x1637) {
		yield();
	}
	od_write(0x6040, 0x00, 0x77);
	while ( (In.StatusWord) != 0x1633) {
		yield();
	}
}

void velocity(U32 param, int sleeptime){
	od_write(0x60FF, 0x00, param);
	sleep(sleeptime);
}