map U16 StatusWord as input 0x6041:00
map U32 Outputs as output 0x60FE:01
#include "wrapper.h"
#include "ioia.h"

void user()
{
	mode_position();
	//mode_velocity();
	start();
	
	//velocity(100, 500);
	target(500);
	target(-250);
	
	stop();
}