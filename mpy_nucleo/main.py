#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import network, time, socket
from machine import UART

net = network.LAN()
status = pyb.LED(1)
error = pyb.LED(3)
error.off()

err = []
log = []
sm = {"system": 0}
socks = {}
serials = {}

machines = [
    #{"part": "left_bowl", "type": "bowl", "connect": "sock", "address": "192.168.126.x"},
    {"part": "left_camera", "type": "camera", "connect": "serial", "uart": 2, "baud": 115200}
    #{"part": "right_bowl", "type": "bowl", "connect": "sock", "address": "192.168.126.x"},
    #{"part": "right_camera", "type": "camera", "connect": "serial", "address": "uart2"},
    #{"part": "scara", "type": "robot", "connect": "sock", "address": "192.168.126.x"}
]

for item in machines:
    #initialize dictionaries strange but works
    add = {item["part"]:0}
    sm.update(add)
    if item["connect"] == "sock":
        add = {item["part"]:None}
        socks.update(add)
    elif item["connect"] == "serial":
        add = {item["part"]:None}
        serials.update(add)

def n_connect():
    try:
        net.active(True)
        net.ifconfig('dhcp')
    except OSError:
        err.append("DHCP timeout, will retry.")
        error.on()
    sm['system']=10

def n_check():
    if net.isconnected():
        log.append("Net address: %s"%str(net.ifconfig()))
        sm['system'] = 11

def heartbeat():
    status.on()
    time.sleep(0.1)
    status.off()
    time.sleep(0.1)

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

def s_test():
    pass
    #s.send(b"GET / HTTP/1.0\r\n\r\n")
    #print(s.recv(4096))

def s_init(part):
    try:
        socks[part] = s_connect("google.com", 80, discover=True, part=part)
    except OSError:
        sm[part]=13
        err.append("%s socket issue."%part)
        error.on()
    sm[part]=10

def u_init(part):
    try:
        add = {item["part"]:UART(item["uart"],item["baud"])}
        serials.update(add)
    except OSError:
        sm[part]=13
        err.append("%s UART issue."%part)
        error.on()
    sm[part]=10

def u_check(part):
    try:
        ser = serials[part]
        ser.write("\n")
        print(ser.readline())
    except OSError:
        sm[part]=13
        err.append("%s UART check issue."%part)
        error.on()
    #sm[part]=11


def init_machines():
    for item in machines:
        if item["connect"] == "sock":
            s_init(item["part"])
        elif item["connect"] == "serial":
            u_init(item["part"])
    sm["system"]=12

def check_machines():
    for item in machines:
        if item["connect"] == "sock":
            pass
        elif item["connect"] == "serial":
            u_check(item["part"])
    #todo
    #if sm['left_bowl']==13 or sm['right_bowl']==13 or sm['left_camera']==13 or sm['right_camera']==13 or sm['scara']==13:
    #    sm["system"]=13
    #if sm['left_bowl']==11 and sm['right_bowl']==11 and sm['left_camera']==11 and sm['right_camera']==11 and sm['scara']==11:
    #    sm["system"]=15

print(sm)

while True:
    heartbeat()
    error.off()
    if sm["system"] == 0:
        n_connect()
    elif sm["system"]==10:
        n_check()
    elif sm["system"]==11:
        init_machines()
    elif sm["system"]==12:
        check_machines()
    else:
        sm['system'] = 13
        error.on()
        break
    print(sm)
    time.sleep(1)

print("\n:( Something went wrong.")
print("\nSystem errors:\n", err)
print("\nSystem log:\n", log)
print("\n\n")
#s.close()
