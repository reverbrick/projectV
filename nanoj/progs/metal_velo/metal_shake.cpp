map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
#include "ioia.h"

void user()
{
	mode_velocity();
	start();
	Out.Outputs = 0x00000;
	sleep(40);
	Out.Outputs = 0x10000;	
	sleep(150);
	Out.Outputs = 0x00000;
	sleep(40);
	Out.Outputs = 0x10000;	
	sleep(150);
	stop();
}