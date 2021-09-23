#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7c
from comms import rmii, Heartbeat
from random import choice
Heartbeat()
rmii("192.168.125.110")
velo = -40 #odd=vibro / even=no vibro

items = [[],[]]
nstats = 5
stats = [[],[]]
avgs = [0, 0]
means = [0, 0]
#cams = [H7c("192.168.125.111", 10001), H7c("192.168.125.121", 10001)]
#bowls = [Nanotec("192.168.125.112"), Nanotec("192.168.125.122")]
scara = Scara("192.168.125.100")
cam = H7c("192.168.125.111", 10001)

"""
for bowl in bowls:
    bowl.velo(velo)
"""
#bowls[0].command("60FE/01","42434242")
#bowls[0].command("60FE/01","42414242")

def main():
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

def snap():
    pos = cam.get()[0];scara.move(pos["x"],pos["y"],pos["angle"])

scara.set_flag(2)

foo = b"\x1b[24;11H\x1b#5S\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;12H\x1b#5H\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;13H\x1b#5O\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;14H\x1b#5W\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;15H\x1b#5 \x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;16H\x1b#5V\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;17H\x1b#5A\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;18H\x1b#5R\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;19H\x1b#5 \x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;20H\x1b#5P\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;21H\x1b#5O\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;22H\x1b#5S\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;23H\x1b#5I\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;24H\x1b#5T\x1b[0;5;7m \x1b[25;81H\x1b[0m\x1b[24;25H\x1b#5 \x1b[25;81H\x1b[04;23r\x1b[23;01H\x1bD\x1b[22;01H\x1b#5SET\x1b[01CVSHOW\x1b[01CVAR\x1b[01CPOSIT\x1b[25;81H\x1b[04;23r\x1b[23;01H\x1bD\x1b[22;05H\x1b#5^\x1b[01CERROR\x1b[25;81H\x1b[23;01H\x1b#5BREAK,\x1b[01CCAMERA,\x1b[01CCLOCK,\x1b[01CDEFAULT,\x1b[01CDISPLAY,\x1b[01CGROUP,\x1b[01CLANG,\x1b[01CLOCAL,\x1b[01CPORT,\x1b[25;81H\x1b[04;23r\x1b[23;01H\x1bD\x1b[23;01H\x1b#5TASK,\x1b[01CTRACE,\x1b[01CVAR,\x1b[01Cor\x1b[01CVERIFY\x1b[01Cexpected.\x1b[25;81H\x1b[04;23r\x1b[23;01H\x1bD\x1b[04;23r\x1b[23;01H\x1bD\x1b[04;23r\x1b[23;01H\x1bD\x1b[24;06H\x1b#5\x1b[0;5;7m \x1b[0m  \x1b[01C     \x1b[01C   \x1b[01C     \x1b[25;81H"

import re
out = foo
out = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', out)
#out = re.sub(' +', ' ', out)
out = str(out).replace("\\x1b m","").replace("\\x1b r","").replace("\\x1b#","").replace("\\x1b","")
#out = str(out).replace("\x1b","")
print(out)

"""
while True:
    scara.move(choice(range(100)),choice(range(100)),choice(range(100)))
    time.sleep(0.5)
    scara.test_pos()
    time.sleep(0.5)

flag = -1
while True:
    try:
        flag = scara.get_flag()
    except:
        pass
    print(flag)
    if flag == '1':
        try:
            pos = cam.get()[0]
            scara.move(pos["x"],pos["y"],pos["angle"])
            time.sleep(0.5)
            scara.set_flag(2)
        except:
            pass
    time.sleep(0.5)
"""
#todo cleanup / restart
#reset()
