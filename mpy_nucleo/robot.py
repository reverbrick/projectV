import urequests as requests

class Scara():
    address = None
    def __init__(self, addr):
        self.address="http://%s"%addr

    def karel_get_numreg(self, index):
        #todo make more general
        res = requests.get('%s/MD/NUMREG.VA'%self.address)
        lines = res.text
        res.close()
        pos= lines.find("[15]")
        return lines[pos+7:pos+8]

    def karel_set_numreg(self, index, real, value):
        r = requests.get('%s/karel/ComSet?sValue=%s&sIndx=%s&sRealFlag=%s&sFc=2'%(self.address, value, index, real))
        r.close()

    def home(self):
        self.karel_set_numreg(15, -1, 0) #flag

    def move(self, x, y, angle):
        self.karel_set_numreg(11, 2, x) #X
        self.karel_set_numreg(12, 2, y) #Y
        self.karel_set_numreg(14, 2, angle) #angle
        self.karel_set_numreg(15, -1, 2) #flag
