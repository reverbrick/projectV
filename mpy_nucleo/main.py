#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import network, time, socket, json
from machine import UART, reset

net = network.LAN()
status = pyb.LED(1)
error = pyb.LED(3)
status.on()
error.off()

retry = 0
max_retry = 10
err = []
log = []
hint = "init"
sm = {"hint": hint, "system": 0}
socks = {}
serials = {}

#machine list
machines = [
    #{"part": "left_bowl", "type": "bowl", "connect": "sock", "address": "192.168.126.x"},
    {"part": "left_camera", "type": "camera", "connect": "serial", "uart": 2, "baud": 115200}
    #{"part": "right_bowl", "type": "bowl", "connect": "sock", "address": "192.168.126.x"},
    #{"part": "right_camera", "type": "camera", "connect": "serial", "address": "uart2"},
    #{"part": "scara", "type": "robot", "connect": "sock", "address": "192.168.126.x"}
]

#initialize dictionaries strange but works
for item in machines:
    add = {item["part"]:0}
    sm.update(add)
    if item["connect"] == "sock":
        add = {item["part"]:None}
        socks.update(add)
    elif item["connect"] == "serial":
        add = {item["part"]:None}
        serials.update(add)

#network connect
def n_connect():
    try:
        net.active(True)
        net.ifconfig('dhcp')
    except OSError:
        #retry = retry + 1
        err.append("DHCP timeout, will retry.")
        error.on()
    sm['system']=10

#network check
def n_check():
    if net.isconnected():
        log.append("Net address: %s"%str(net.ifconfig()))
        sm['system'] = 11

#flash the green led
def heartbeat():
    status.on()
    time.sleep(0.1)
    status.off()
    time.sleep(0.1)

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
    pass
    #s.send(b"GET / HTTP/1.0\r\n\r\n")
    #print(s.recv(4096))

#socket establishing
def s_init(part):
    try:
        socks[part] = s_connect("google.com", 80, discover=True, part=part)
    except OSError:
        #retry = retry + 1
        sm[part]=13
        err.append("%s socket issue."%part)
        error.on()
    sm[part]=10

#UART establishing
def u_init(part):
    try:
        add = {item["part"]:UART(item["uart"],item["baud"])}
        serials.update(add)
    except OSError:
        #retry = retry + 1
        sm[part]=13
        err.append("%s UART issue."%part)
        error.on()
    sm[part]=10

#UART check
def u_check(part):
    try:
        ser = serials[part]
        ser.write("\n")
        r = ser.readline()
        if r:
            #check if response is valid json
            ret = json.loads(r)
            sm[part]=11
    except OSError:
        #retry = retry + 1
        sm[part]=13
        err.append("%s UART check issue."%part)
        error.on()

#Query camera via UART
def u_get(part):
    ret = None
    try:
        ser = serials[part]
        ser.write("\n")
        r = ser.readline()
        if r:
            ret = json.loads(r)
    except OSError:
        #retry = retry + 1
        err.append("%s UART get issue."%part)
        error.on()
    return ret

#Initialize all listed machines
def init_machines():
    for item in machines:
        if item["connect"] == "sock":
            s_init(item["part"])
        elif item["connect"] == "serial":
            u_init(item["part"])
    sm["system"]=12

#Check all listed machines
def check_machines():
    #do checks
    for item in machines:
        if item["connect"] == "sock":
            pass
        elif item["connect"] == "serial":
            u_check(item["part"])
    #check results
    good = True
    for item in machines:
        if sm[item["part"]]==11:
            #all should be 11
            pass
        else:
            good = False
    if good:
        sm["system"]=15
    else:
        pass
        #todo recheck??
        #retry = retry + 1
        #sm["system"]=13

def run_machines():
    print(u_get("left_camera"))

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
        init_machines()
    elif sm["system"]==12:
        hint = "machines init -> check machines"
        check_machines()
    elif sm["system"]==15:
        hint = "machines ready -> run machines"
        run_machines()
    else:
        hint = "no such state -> error state"
        sm['system'] = 13
        error.on()
        break
    sm["hint"] = hint
    #sm["retry"] = retry
    print(sm)
    time.sleep(0.3)

#dump
print("\n:( Something went wrong.")
print("\nSystem errors:\n", err)
print("\nSystem log:\n", log)
print("\n\n")

#todo cleanup / restart
#s.close()
reset()
