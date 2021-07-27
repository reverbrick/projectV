#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import socket

class Nanotec():
    host = None
    def __init__(self, host):
        self.host=host

    def hex3(self, n):
        return str("0x%s"%("00000000%x"%(n&0xffffffff))[-8:]).upper()[2:]

    def command(self, addr, val):
        #os.system("""curl -H "Content-Type: application/x-www-form-urlencoded" -d '"%s"' -X POST  %s/od/%s"""%(val,self.host,addr))
        #todo fix content lenfth
        req = b'POST /od/%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: IOIA\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 10\r\n\r\n"%s" = '%(addr,self.host,val)
        address = (self.host, 80)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.send(req)
        sock.close()

    def ready(self):
        self.command("6040/00","0006")

    def on(self):
        self.command("6040/00","0007")

    def run(self):
        self.command("6040/00","000F")

    def stop(self):
        self.command("6040/00","0000")

    def velo(self, val):
        self.command("60FF/00", self.hex3(val))

    def accel(self, val):
        self.command("60C5/00", self.hex3(val))

    def decel(self, val):
        self.command("60C6/00", self.hex3(val))

    def prog(self):
        self.command("2300/00", self.hex3(1))
