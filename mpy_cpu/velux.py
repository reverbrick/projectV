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
scara = {}

def test():
    while True:
        bowls[0].prog()
        bowls[1].prog()
        #print(0,getItems(0))
        #print(1,getItems(1))
        #print(shake(1))
        time.sleep(0.7)

def shake(id, sleep=0.4):
    """
    ret = []
    retry = 1
    while ret==[]:
        print("retry #%s"%retry)
        bowls[id].prog()
        time.sleep(sleep)
        ret = cams[id].get()
    """
    bowls[id].prog()
    time.sleep(sleep)
    ret = cams[id].get()
    return ret

def getItems(id):
    #initial shaking
    if items[id] == []:
        items[id] = shake(id)
    #pick one from the list
    if items[id]!=[]:
        pos = items[id].pop(0)
    else:
        pos = {}
    """
    #picked last one shake again
    if items[id] == []:
        items[id] = shake(id)
    """
    print(pos)
    if pos!={}:
        return "'%s''%s''%s''%s'\r\n"%(pos["x"], pos["y"], pos["angle"], pos["side"])
    else:
        return "'0''0''0''-1'\r\n"
        #return "''''''''\r\n"

while(True):
    c, addr = s.accept()
    print("connected %s"%addr[0])
    scara[addr[0]] = c.makefile()
    #try:
    message = scara[addr[0]].recv(1024)
    print(message)
    if message == b'\x00\x07snap0\r':
        items = [[],[]]
        scara[addr[0]].write("'0''0''0''0'\r\n")
    elif message == b'\x00\x07snap1\r':
        scara[addr[0]].write(getItems(0))
    elif message == b'\x00\x07snap2\r':
        scara[addr[0]].write(getItems(1))
    """
    #wait till state change
    retry = 0
    while "state=3" in str(scara[addr[0]]):
        print(scara[addr[0]])
        print(".", end="")
        retry=retry+1
        time.sleep_ms(30)
        if retry>20:
            break
    """
    scara[addr[0]].recv(1024) 
    c.close()
    #except:
    #    machine.reset
