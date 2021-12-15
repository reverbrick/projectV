#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import struct
import network, time, pyb
import libs.utelnet as telnet

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.send(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    try:
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
    except OSError:
        pass
    return data

class Heartbeat(object):
    def __init__(self):
        self.tick = 0
        self.led = pyb.LED(1)
        tim = pyb.Timer(4)
        tim.init(freq=10)
        tim.callback(self.heartbeat_cb)

    def heartbeat_cb(self, tim):
        if self.tick <= 3:
            self.led.toggle()
        self.tick = (self.tick + 1) % 10

def wiznet(ip):
    net = network.WIZNET5K(pyb.SPI(2), pyb.Pin.board.D10, pyb.Pin.board.D13)
    net.active(True)
    net.ifconfig((ip, '255.255.255.0', '192.168.125.1', '192.168.125.1'))

    while not net.isconnected():
        time.sleep(0.1)

    print(net.ifconfig())
    telnet.start()

def rmii(ip):
    net = network.LAN()
    net.active(True)
    net.ifconfig((ip, '255.255.255.0', '192.168.125.1', '192.168.125.1'))

    while not net.isconnected():
        time.sleep(0.1)

    print(net.ifconfig())
    telnet.start()
