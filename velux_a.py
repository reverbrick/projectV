#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time
from machine import reset
from libs.robot import Scara
from libs.stepper import Nanotec
from libs.camera import H7c
from libs.comms import rmii, Heartbeat
from random import choice
Heartbeat()
rmii("192.168.125.150")

import uasyncio as asyncio


#@asyncio.coroutine
def serve(reader, writer):
    #print(reader, writer)
    #print("================")
    print((yield from reader.read(256)))
    yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello.\r\n")
    yield from writer.aclose()
    #print("Finished processing request")

loop = asyncio.get_event_loop()
#mem_info()
loop.create_task(asyncio.start_server(serve, "0.0.0.0", 8081, backlog=100))
loop.run_forever()
loop.close()
