#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import network, time
import utelnet.utelnetserver as telnet
from machine import reset
from robot import Scara
from stepper import Nanotec
from camera import H7

net = network.LAN()
net.active(True)
net.ifconfig(('192.168.125.110', '255.255.255.0', '192.168.125.1', '8.8.8.8'))

print("Waiting for net...")

if net.isconnected():
    telnet.start()
    l_cam = H7("192.168.125.111", 10001)
    l_bow = Nanotec("192.168.125.112")
    scara = Scara("192.168.125.100")

#dump
#print("\n:( Something went wrong.")
#print("\nSystem errors:\n", err)
#print("\nSystem log:\n", log)
#print("\n\n")

#todo cleanup / restart
#reset()
