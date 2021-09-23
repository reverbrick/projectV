#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7
from comms import wiznet, Heartbeat
Heartbeat()
wiznet("192.168.125.110")

items = [[],[]]
stats = [[],[]]
avgs = [0, 0]
cams = [H7("192.168.125.111", 10001)]#, H7("192.168.125.121", 10001)]
bowls = [Nanotec("192.168.125.112"), Nanotec("192.168.125.122")]
#scara = Scara("192.168.125.100")

for bowl in bowls:
    pass
    #bowl.velo(50)

while True:
    for id, cam in enumerate(cams):
        if items[id] == []:
            try:
                pass
                #bowls[id].prog()
            except OSError:
                print("Bowl #%s not responding. Will wait 5 secs and reset."%id)
                time.sleep(5)
                reset()
            try:
                items[id] = cam.get()
            except OSError:
                print("Camera #%s not responding. Will wait 5 secs and reset."%id)
                time.sleep(5)
                reset()
            if len(stats[id]) > 5: #how many stats
                stats[id].pop(0)
            stats[id].append(len(items[id]))
            avgs[id] = round(sum(stats[id])/len(stats[id]),1)
        else:
            flag = 0 #todo getting proper flag
            if (id == 0 and flag == "get0") or (id == 1 and flag == "get1"):
                pos = items[id].pop(0)
                try:
                    scara.move(pos["x"], pos["y"], pos["angle"])
                except OSError:
                    print("Scara not responding. Will wait 5 secs and reset.")
                    time.sleep(5)
                    reset()
    print(items, avgs)

#todo cleanup / restart
#reset()
