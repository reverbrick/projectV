#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
from machine import UART
import time, re, gc

class Scara():
    sock = None

    def flush(self):
        r = self.sock.readline()
        print("flush:", end="")
        while r == None:
            time.sleep_ms(10)
            r = self.sock.readline()
            print(".", end="")
        print("OK")

    def send(self, what, flush=False):
        print("send",what)
        self.sock.write("%s"%what)
        if flush:
            self.flush()

    def readuntil(self, what, max=100):
        found = False
        retry = 0
        out = None
        while True:
            r = self.sock.read(4096)
            if r:
                #print("recv",r)
                if what in r:
                    found = True
                    out = r
                    break
            elif r==None:
                print(".", end="")
                retry = retry + 1
                if retry == max:
                    break
            time.sleep_ms(10)
        print("OK")
        if found==False:
            print("Error in", what, out)
        return (found, r)

    def __init__(self, addr):
        self.sock = UART(3, 115200)
        self.sock.writechar(4) #disconnect
        time.sleep(0.1)
        self.sock.write("C%s/23\n"%addr) #connect
        if self.readuntil("login:")[0]==True:
            self.send("KCL\n")
            if self.readuntil("password:")[0]==True:
                self.send("1111\n")
                if self.readuntil("User logged in")[0]==True:
                    self.send("SET DEFAULT przerzutki2\r\n", flush=True)

    def set_flag(self, val):
        self.send("SET VAR FLAG_IN=%s\r\n"%val, flush=True)

    def get_flag(self):
        self.send("SHOW VAR FLAG_OUT\r\n\r\n")
        out = ""
        ret = self.readuntil("Storage:", max=50)
        rep = ["\\x1b m","\\x1b r","\\x1b#","\\x1b","[25;8","H[04;","r[23;01HD[22;64H51231H'"]
        if ret[0]:
            out = str(ret[1])
            for x in rep:
                out = out.replace(x,"")
            out = out[out.find("=")+1:]
        return out

    def move(self, x, y, angle):
        self.send("SET VAR POSIT=%s,%s,0,0,0,%s\r\n"%(x,y,angle),flush=True)
