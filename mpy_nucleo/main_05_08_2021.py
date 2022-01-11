#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import network, time
import utelnet.utelnetserver as telnet
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7
from common import heartbeat, run, error

net = network.LAN()
pause = 0.5
retry = 0
max_retry = 10
err = []
log = []
hint = "init"
sm = {"hint": hint, "system": 0}
socks = {}
serials = {}

#machine list
machines = {
    "left_bowl": {"type": "bowl", "address": "192.168.125.233"},
    "left_camera": {"type": "camera", "address": "192.168.125.150", "port": 10001},
    #"right_bowl": {"type": "bowl","address": "192.168.125.234"},
    #"right_camera": {"type": "camera", "uart": 5, "baud": 115200},
    #"scara": {"type": "robot", "address": "192.168.125.100"}
}

#initialize dictionaries strange but works
for key in machines:
    item = machines[key]
    add = {key:0}
    sm.update(add)

#network connect
def n_connect():
    try:
        net.active(True)
        #net.ifconfig('dhcp')
        net.ifconfig(('192.168.125.125', '255.255.255.0', '192.168.125.1', '8.8.8.8'))
    except OSError:
        #retry = retry + 1
        err.append("DHCP timeout, will retry.")
        #error.on()
    sm['system']=10

#network check
def n_check():
    if net.isconnected():
        telnet.start()
        log.append("Net address: %s"%str(net.ifconfig()))
        sm['system'] = 11

####cleaned
def machine_init(key = "all"):
    if key == "all":
        for key in machines:
            try:
                machine_init(key = key)
            except OSError:
                sm[key]=13
                sm['system'] = 13
                err.append("%s init issue."%key)
                #error.on()
            sm['system'] = 12
    else:
        item = machines[key]
        if item["type"] == "camera":
            item["obj"]=H7(item["address"], item["port"])
        elif item["type"] == "robot":
            item["obj"]=Scara(item["address"])
        elif item["type"] == "bowl":
            item["obj"]=Nanotec(item["address"])
        sm[key]=10

def machine_check(key = "all"):
    if key == "all":
        for key in machines:
            try:
                machine_check(key = key)
            except OSError:
                sm[key]=13
                sm['system'] = 13
                err.append("%s check issue."%key)
                #error.on()TaskQueue = [ heartbeat() ]
            sm['system'] = 15
    else:
        item = machines[key]
        if item["type"] == "camera":
            pass
        elif item["type"] == "robot":
            pass
        elif item["type"] == "bowl":
            item["obj"].ready()
        sm[key]=11

def machine_run():
    run()
    try:
        #robot = machines["scara"]["obj"]
        l_cam = machines["left_camera"]["obj"]
        l_bowl = machines["left_bowl"]["obj"]
        #robot.home()
        l_bowl.prog()
        time.sleep(1.6)
        positions = l_cam.get()
        if positions:
            for pos in positions:
                print("going to: ", pos)
                #robot.move(pos["x"],pos["y"],pos["angle"])
    except KeyError:
        #not all machines present
        reset()
    except OSError:
        print("move failed")

#print initial state machine
def StateMachine():
    while True:
        if sm["system"] == 0:
            hint = "initialized -> connect network"
            n_connect()
        elif sm["system"]==10:
            hint = "network connected -> check network"
            n_check()
        elif sm["system"]==11:
            hint = "network ready -> init machines"
            machine_init()
        elif sm["system"]==12:
            hint = "machines init -> check machines"
            machine_check()
        elif sm["system"]==15:
            hint = "machines ready -> run machines"
            machine_run()
        else:
            hint = "no such state -> error state"
            sm['system'] = 13
            #error.on()
            TaskQueue = [ error() ]
        sm["hint"] = hint
        #sm["retry"] = retry
        print(sm)
        yield None

TaskQueue = [ heartbeat(), StateMachine()]
print("Waiting 5secs for everything to boot up.")
time.sleep(5)
print(sm)
#main loop
while True:
    for task in TaskQueue:
        next(task)
    time.sleep(pause)

#dump
print("\n:( Something went wrong.")
print("\nSystem errors:\n", err)
print("\nSystem log:\n", log)
print("\n\n")

#todo cleanup / restart
reset()
