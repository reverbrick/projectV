#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import socket, json, re, time
from comms import send_msg, recv_msg

class H7():
    sock = None
    def __init__(self, host, port):
        self.connect(host, port)

    #socket connection helper
    def connect(self, host, port, discover=False):
        self.sock = socket.socket()
        if discover:
            ai = socket.getaddrinfo(host, port)
            addr = ai[0][-1]
        else:
            addr = (host, port)
        self.sock.connect(addr)
        self.sock.setblocking(False)

    def get(self):
        ret = None
        send_msg(self.sock,b"snap")
        for i in range(3):
            time.sleep(1)
            r = str(recv_msg(self.sock))
            if r:
                break
        #print(r)
        if r!=None:
            m = re.search(r"\[(.*?)\]",r)
            if m:
                r = m.group(0)
            if r:
                ret = json.loads(r)
        #except:
        #    pass
        return ret
