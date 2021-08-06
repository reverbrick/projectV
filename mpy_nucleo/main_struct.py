import socket, time, struct
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#addr = ("192.168.125.110", 23)
#sock.connect(addr)
#sock.setblocking(False)
sock.bind(("192.168.125.110",10001))

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

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
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

while True:
    recv_msg(sock)
    #recvall(sock,1024)
    time.sleep(1)
