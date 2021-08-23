import struct

def send_msg(ser, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    ser.write(msg)

def recv_msg(ser):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(ser, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(ser, msglen)

def recvall(ser, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    try:
        while len(data) < n:
            packet = ser.read(n - len(data))
            if not packet:
                return None
            data.extend(packet)
    except MemoryError:
        pass
    return data
