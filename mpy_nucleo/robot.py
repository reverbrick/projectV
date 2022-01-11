#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import socket

class Scara():
    sock = None
    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, 23))
        self.sock.setblocking(False)
        readuntil(self.sock,"login:")
        self.sock.send(b"KCL\r\n")
        readuntil(self.sock,"password:")
        self.sock.send(b"1111\r\n")
        readuntil(self.sock,"User logged in")
        self.sock.send(b"SET DEFAULT przerzutki\r\n")
        readuntil(self.sock,"SET DEFAULT przerzutki")

    def set_flag(self, val):
        self.sock.send(b"SET VAR FLAG_IN=2\r\n")

    def move(self, x, y, angle):
        self.sock.send(b"SET VAR POS=%s,%s,0,%s,0,0\r\n")
