#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
#refer to states.txt for state machine explanations
import time, socket
from comms import rmii
rmii("192.168.125.110")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.125.100", 23))
sock.setblocking(False)
