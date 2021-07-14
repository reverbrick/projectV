#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import urequests as requests

class Nanotec():
    #host = "http://192.168.89.233"
    host = None
    def __init__(self, host):
        self.host="http://%s"%host

    def hex3(self, n):
        return str("0x%s"%("00000000%x"%(n&0xffffffff))[-8:]).upper()[2:]

    def command(self, addr, val):
        #os.system("""curl -H "Content-Type: application/x-www-form-urlencoded" -d '"%s"' -X POST  %s/od/%s/00"""%(val,self.host,addr))
        r = requests.post("%s/od/%s/00"%(self.host,addr),data='"%s"'%val)
        r.close()

    def ready(self):
        self.command("6040","0006")

    def on(self):
        self.command("6040","0007")

    def run(self):
        self.command("6040","000F")

    def stop(self):
        self.command("6040","0000")

    def velo(self, val):
        self.command("60FF", self.hex3(val))

    def accel(self, val):
        self.command("60C5", self.hex3(val))

    def decel(self, val):
        self.command("60C6", self.hex3(val))
