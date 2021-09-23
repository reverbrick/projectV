map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
void user()
{
	// Set mode "Profile velocity"
	od_write(0x6060, 0x00, 3);

	// Remember target velocity 
	U32 targetVelocity = od_read(0x60FF, 0x00);

	// Set the target velocity
	od_write(0x60FF, 0x00, targetVelocity);

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

	// Let the motor run for a while
	Out.Outputs = 0x00000;
	sleep(50);
	Out.Outputs = 0x10000;
	sleep(50);
	Out.Outputs = 0x00000;
	sleep(50);
	Out.Outputs = 0x10000;	
	sleep(200);
	od_write(0x60FF, 0x00, targetVelocity*-1);
	sleep(300);
	od_write(0x60FF, 0x00, targetVelocity);
	sleep(300);
	od_write(0x60FF, 0x00, targetVelocity*-1);
	sleep(600);
	od_write(0x60FF, 0x00, targetVelocity);

	// Stop the motor
	od_write(0x6040, 0x00, 0x0);

	// Stop the NanoJ program. Without this line, the firmware would
	// call user() again as soon as we return.
	od_write(0x2300, 0x00, 0x0);
}