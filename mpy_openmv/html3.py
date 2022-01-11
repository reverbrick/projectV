import ubinascii, json
from machine import UART
from ioia import Camera, Flash, Velux; import time
from comms import recv_msg, send_msg
cam = Camera(exposure=50000, framesize="QQQVGA")
cam.sensor.set_quality(100)
fla = Flash(100,0)
cli = Velux()
ser = UART(3, 921600)

resp = b"""HTTP/1.0 200 OK
Content-Type: multipart/x-mixed-replace; boundary="frame"

"""
resp2 = b"""--frame
Content-type: text/html

<img src="data:image/jpeg;base64, %s"/>

"""


def write(arr):
    print(arr)
    ser.write(arr)

while(True):
    req = ser.read(4096)
    if req:
        if b"GET" in req:
            write(resp)
            while(True):
                img = cam.snap(fla, corr=0.9)
                write(resp2%ubinascii.b2a_base64(img.compress(quality=90)))
                time.sleep(0.5)
    time.sleep(0.1)
