map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
void user()
{
	// Set mode "Profile velocity 3"
	od_write(0x6060, 0x00, 0x1);
 	// Request state "Ready to switch on"
	od_write(0x6040, 0x00, 0x6);
	// Wait until the requested state is reached
	while ( (In.StatusWord & 0xEF) != 0x21) {
		yield(); // Wait for the next cycle (1ms)
	}
	// Request the state "Switched on"
	od_write(0x6040, 0x00, 0x7);
	// Wait until the requested state is reached
	while ( (In.StatusWord & 0xEF) != 0x23) {
		yield();
	}
	// Request the state "Operation enabled"
	od_write(0x6040, 0x00, 0xF);
	// Wait until the requested state is reached
	while ( (In.StatusWord & 0xEF) != 0x27) {
		yield();
	}
	
	od_write(0x607A, 0x00, 0x1f4); //terget position
	od_write(0x6040, 0x00, 0x7F);
	// Wait until the requested state is reached
	while ( (In.StatusWord) != 0x1637) {
		yield();
	}
	od_write(0x6040, 0x00, 0x77);
	// Wait until the requested state is reached
	while ( (In.StatusWord) != 0x1633) {
		yield();
	}
	od_write(0x607A, 0x00, 0xFFFFFF9C); //terget position
	od_write(0x6040, 0x00, 0x7F);
	// Wait until the requested state is reached
	while ( (In.StatusWord) != 0x1637) {
		yield();
	}
	
	// Stop the motor
	od_write(0x6040, 0x00, 0x0);

	// Stop the NanoJ program. Without this line, the firmware would
	// call user() again as soon as we return.
	od_write(0x2300, 0x00, 0x0);
}