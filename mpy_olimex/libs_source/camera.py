#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import socket, json, re, time
from libs.comms import send_msg, recv_msg

class H7():
    host = None
    port = None
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5.0)
        self.sock.connect((host, port))

    def get(self):
        ret = []

        send_msg(self.sock,b"snap")
        r = str(recv_msg(self.sock))
        if r!=None:
            m = re.search(r"\[(.*?)\]",r)
            if m:
                r = m.group(0)
                if r:
                    ret = json.loads(r)
        return ret

class H7c():
    host = None
    port = None
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get(self):
        ret = []
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((self.host, self.port))
        send_msg(sock,b"snap")
        r = str(recv_msg(sock))
        if r!=None:
            m = re.search(r"\[(.*?)\]",r)
            if m:
                r = m.group(0)
                if r:
                    ret = json.loads(r)
        sock.close()
        return ret
