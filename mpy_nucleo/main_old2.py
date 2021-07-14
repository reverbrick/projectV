#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import network, time, socket, json
from machine import UART, reset
#import utelnet.utelnetserver as telnet
from robot import Scara
from stepper import Nanotec

net = network.LAN()
status = pyb.LED(1)
work = pyb.LED(2)
error = pyb.LED(3)
status.on()
error.off()
work.off()

pause = 0.3
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
    "left_bowl": {"type": "bowl", "connect": "nanotec", "address": "192.168.125.233"},
    "left_camera": {"type": "camera", "connect": "serial", "uart": 2, "baud": 115200},
    "right_bowl": {"type": "bowl", "connect": "nanotec", "address": "192.168.125.234"},
    "right_camera": {"type": "camera", "connect": "serial",  "uart": 5, "baud": 115200},
    "scara": {"type": "robot", "connect": "karel", "address": "192.168.125.100"}
}

#initialize dictionaries strange but works
for key in machines:
    item = machines[key]
    add = {key:0}
    sm.update(add)


async def blink(led):
    while True:
        led.on()
        await uasyncio.sleep_ms(5)
        led.off()
        await uasyncio.sleep_ms(700)

#network connect
def n_connect():
    try:
        net.active(True)
        net.ifconfig('dhcp')
        #net.ifconfig(('192.168.125.125', '255.255.255.0', '192.168.125.1', '8.8.8.8'))
    except OSError:
        #retry = retry + 1
        err.append("DHCP timeout, will retry.")
        error.on()
    sm['system']=10

#network check
def n_check():
    if net.isconnected():
        #telnet.start()
        log.append("Net address: %s"%str(net.ifconfig()))
        sm['system'] = 11

#flash the green led
def heartbeat():
    status.on()
    time.sleep(0.01)
    status.off()
    time.sleep(0.01)

def run():
    work.on()
    time.sleep(0.01)
    work.off()
    time.sleep(0.01)

#socket connection helper
def s_connect(host, port, discover=False, part=None):
    s = socket.socket()
    if discover:
        ai = socket.getaddrinfo(host, port)
        log.append("%s infos: %s"%(part,str(ai)))
        addr = ai[0][-1]
    else:
        addr = (host, port)
    log.append("%s address: %s"%(part,str(addr)))
    s.connect(addr)
    return s

#socket check
def s_test():
    #pass
    s.send(b"GET / HTTP/1.0\r\n\r\n")
    print(s.recv(4096))

#socket establishing
def s_init(part):
    try:
        socks[part["part"]] = s_connect(part["address"], 80, discover=False, part=part["part"])
    except OSError:
        #retry = retry + 1
        sm[part["part"]]=13
        err.append("%s socket issue."%part["part"])
        error.on()
    sm[part["part"]]=10

#Query camera via UART
def u_get(part):
    ret = None
    try:
        ser = machines[part]["obj"]
        ser.write("\n")
        r = ser.readline()
        if r:
            ret = json.loads(r)
    except ValueError:
        err.append("%s UART get issue."%part)
        error.on()
    except OSError:
        err.append("%s UART get issue."%part)
        error.on()
    return ret

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
                error.on()
            sm['system'] = 12
    else:
        item = machines[key]
        if item["connect"] == "sock":
            #todo
            pass
        elif item["connect"] == "serial":
            item["obj"]=UART(item["uart"], item["baud"])
        elif item["connect"] == "karel":
            item["obj"]=Scara(item["address"])
        elif item["connect"] == "nanotec":
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
                error.on()
            sm['system'] = 15
    else:
        item = machines[key]
        if item["connect"] == "sock":
            pass
        elif item["connect"] == "serial":
            pass
        elif item["connect"] == "karel":
            pass
        elif item["connect"] == "nanotec":
            pass
        sm[key]=11

def machine_run():
    run()
    robot = machines["scara"]["obj"]
    try:
        #robot.home()
        print(u_get("left_camera"))
    except OSError:
        print("move failed")

#print initial state machine
print(sm)

#main loop - state machine
while True:
    #too much retries
    #if retry > max_retry:
    #    sm['system'] = 13
    heartbeat()
    error.off()
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
        #machine_run()
        break
    else:
        hint = "no such state -> error state"
        sm['system'] = 13
        error.on()
        break
    sm["hint"] = hint
    #sm["retry"] = retry
    print(sm)
    time.sleep(pause)

#dump
#print("\n:( Something went wrong.")
#print("\nSystem errors:\n", err)
#print("\nSystem log:\n", log)
#print("\n\n")

#todo cleanup / restart
#s.close()
#reset()
