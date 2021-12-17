map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
#include "ioia.h"

void user()
{
	ClearDigitalOutput(2);
	mode_velocity();
	start();
	ClearDigitalOutput(1);
	sleep(40);
	SetDigitalOutput(1);
	sleep(100);
	ClearDigitalOutput(1);
	sleep(40);	
	SetDigitalOutput(1);
	sleep(100);
	ClearDigitalOutput(1);
	sleep(40);	
	SetDigitalOutput(1);
	sleep(100);
	od_write(0x6040, 0x00, 0x0);
	sleep(1500);
	SetDigitalOutput(2);
	//stop();
	od_write(0x2300, 0x00, 0x0);
}