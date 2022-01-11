#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7c
from comms import wiznet, Heartbeat
Heartbeat()
wiznet("192.168.125.110")
velo = -40 #odd=vibro / even=no vibro

items = [[],[]]
nstats = 5
stats = [[],[]]
avgs = [0, 0]
means = [0, 0]
cams = [H7c("192.168.125.111", 10001), H7c("192.168.125.121", 10001)]
bowls = [Nanotec("192.168.125.112"), Nanotec("192.168.125.122")]
#scara = Scara("192.168.125.100")

for bowl in bowls:
    bowl.velo(velo)

#bowls[0].command("60FE/01","42434242")
#bowls[0].command("60FE/01","42414242")

while True:
    for id, cam in enumerate(cams):
        if True:#items[id] == []:
            try:
                if avgs[id]<1:
                    bowls[id].velo(velo+1) #switch vibro on
                else:
                    bowls[id].velo(velo)
                bowls[id].prog()
                time.sleep(1)
            except OSError:
                print("Bowl #%s not responding. Will wait 5 secs and reset."%id)
                time.sleep(5)
                #reset()
            try:
                if id==0:
                    items[id] = cam.get()
                    if len(items[id])!=0:
                        means[id]=items[id][0]["mean"]
            except OSError:
                print("Camera #%s not responding. Will wait 5 secs and reset."%id)
                time.sleep(5)
                #reset()
            if len(stats[id]) > nstats:
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
                    #reset()
    print(items, avgs, means)

#todo cleanup / restart
#reset()
