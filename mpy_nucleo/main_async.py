#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time
import utelnet.utelnetserver as telnet
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7
from common import heartbeat, run, error
import uasyncio as asyncio

pause = 0.5
retry = 0
max_retry = 10
err = []
log = []
hint = "init"
sm = {"hint": hint, "system": 0}
socks = {}
serials = {}

#interface = rpc.rpc_wifi_or_ethernet_master("192.168.125.111")

#machine list
machines = {
    "left_camera": {"type": "camera", "address": "192.168.125.111", "port": 10001},
    "left_bowl": {"type": "bowl", "address": "192.168.125.112"},
    #"right_camera": {"type": "camera", "address": "192.168.125.121", "port": 10001},
    #"right_bowl": {"type": "bowl", "address": "192.168.125.122"},
    #"scara": {"type": "robot", "address": "192.168.125.100"}
}

#initialize dictionaries strange but works
for key in machines:
    item = machines[key]
    add = {key:0}
    sm.update(add)

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

def machine(item):
    return machines[item]["obj"]

def machine_run():
    run()
    try:
        #robot = machines["scara"]["obj"]
        l_cam = machine("left_camera")
        l_bowl = machine("left_bowl")
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

print(sm)

def print_http_headers(url):
    reader, writer = yield from asyncio.open_connection(url, 80)
    print("================")
    query = "GET / HTTP/1.0\r\n\r\n"
    yield from writer.awrite(query.encode('latin-1'))
    while True:
        line = yield from reader.readline()
        if not line:
            break
        if line:
            print(line.rstrip())
    print(dir(asyncio))

loop = asyncio.get_event_loop()
#task = asyncio.async(print_http_headers(url))
#loop.run_until_complete(task)
#loop.run_until_complete(print_http_headers("192.168.125.112"))
loop.run_until_complete(machine_init())

loop.close()

#dump
#print("\n:( Something went wrong.")
#print("\nSystem errors:\n", err)
#print("\nSystem log:\n", log)
#print("\n\n")

#todo cleanup / restart
#reset()
