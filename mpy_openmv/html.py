import ubinascii, json
from machine import UART
from ioia import Camera, Flash, Velux; import time
from comms import recv_msg, send_msg
cam = Camera(exposure=50000, framesize="QQQVGA")
cam.sensor.set_quality(100)
fla = Flash(100,0)
cli = Velux()
ser = UART(3, 921600)

resp = b"""HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n"""
html = b"""<img src="data:image/jpeg;base64, %s"/>"""

while(True):
    req = ser.read(4096)
    if req:
        if b"GET" in req:
            img = cam.snap(fla, corr=0.9)
            ser.write(resp)
            ser.write(html%ubinascii.b2a_base64(img.compress(quality=90)))
    time.sleep(0.1)
