#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time, socket, machine
from libs.camera import H7c
from libs.stepper import Nanotec
from libs.comms import rmii, Heartbeat
Heartbeat()
rmii("192.168.125.110")

items = [[],[]]
cams = [H7c("192.168.125.111", 10001), H7c("192.168.125.121", 10001)]
bowls = [Nanotec("192.168.125.112"), Nanotec("192.168.125.122")]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("",7776))
s.listen(5)
print("ready")

def getItems(id):
    if items[id] == []:
        #bowls[id].prog()
        #time.sleep(1)
        items[id] = cams[id].get()
    pos = items[id].pop(0)
    print(pos)
    if pos!=[]:
        return "'%s''%s''%s'\r\n"%(pos[0]["x"], pos[0]["y"], pos[0]["angle"])
    else:
        return "''''''\r\n"

while(True):
    c, addr = s.accept()
    print("connected")
    scara = c.makefile()
    #try:
    message = scara.recv(1024)
    print(message)
    if message == b'\x00\x07snap1\r':
        scara.write(getItems(0))
    elif message == b'\x00\x07snap2\r':
        scara.write(getItems(1))
    time.sleep(1) #do not delete
    c.close()
    """
    except:
        machine.reset()
    """
