#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
from machine import UART
import time, re, gc

class Scara():
    sock = None

    def pretty(self, out):
        """
        gc.collect()
        out =""
        rem = ["[2J[1;1f","[01C","[02C","[25;81H","[23;54H#5","[23;62H#5","[23;01H#5","[04;23r","[23;01HD","[22;01H#5","[0m","[24;07H#5H","[22;64H#5","[24;06H#5","[0;5;7m","[24;08H#5O","[24;09H#5W","[24;10H#5","[24;11H#5V","[24;12H#5A","[24;13H#5R","[24;14H#5","[24;15H#5F","[24;16H#5L","[24;17H#5A","[24;18H#5G","[24;19H#5_","[24;20H#5O","[24;21H#5U","[24;22H#5T","[24;23H#5"]
        for c in list(x):
            if c<127 and c>31:
                out = out + chr(c)
        for c in rem:
            out=out.replace(c," ")
        """
        #out = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', out)
        #out = re.sub(' +', ' ', out)
        out = str(out).replace("\\x1b m","").replace("\\x1b r","").replace("\\x1b#","").replace("\\x1b","")
        #out = str(out).replace("\x1b","")
        return out

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
            r = self.sock.readline()
            if r:
                #print("recv",self.pretty(r))
                print("recv",r)
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
        #print(re.sub(r"(\\x1b\[|\\x1b#)[0-?]*[ -\/]*[@-~]", '', self.readuntil(self.sock,"81H")))
        #ansi_escape =re.compile(br'(\x1b\[)[0-?]*[ -\/]*[@-~]')
        #print(ansi_escape.sub(b'', self.readuntil(self.sock,"81H")))
        #x = self.sock.readline()
        """
        if x:
            out = self.pretty(x)
            return out[out.find("INTEGER = ")+10:].strip()
        self.readuntil("FLAG_OUT")
        """
        print(self.readuntil("INTEGER", max=50))
        return None

    def move(self, x, y, angle):
        self.send("SET VAR POSIT=%s,%s,0,0,0,%s\r\n"%(x,y,angle),flush=True)

    def test_pos(self):
        self.send("SHOW VAR POSIT\r\n")
        self.readuntil("POSIT")
