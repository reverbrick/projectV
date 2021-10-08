map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
#include "ioia.h"

void user()
{
	mode_position();
	start();
	Out.Outputs = 0x00000;
	sleep(50);
	Out.Outputs = 0x10000;
	target(-500);
	//sleep(50);
	stop();
}