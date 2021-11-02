import ubinascii, json, omv
from machine import UART
import time, sensor
omv.disable_fb(True)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.SXGA)
sensor.skip_frames(time = 2000)
ser = UART(3, 921600)

resp = b"""HTTP/1.1 200 OK\r\nConnection: Close\r\nContent-type: %s\r\nContent-Length: %s\r\n\r\n%s\x04"""

while(True):
    req = ser.readline()
    if req:
        if b"GET /img" in req:
            img = sensor.snapshot().copy(x_size=640, copy_to_fb=True).compress(quality=50)
            data = ubinascii.a2b_base64((ubinascii.b2a_base64(img)))
            ser.write(resp%("image/jpeg",len(data),data))
        elif b"GET /roi" in req:
            img = sensor.snapshot().copy(roi=(320,256,640,512), copy_to_fb=True).compress(quality=50)
            data = ubinascii.a2b_base64((ubinascii.b2a_base64(img)))
            ser.write(resp%("image/jpeg",len(data),data))
        elif b"GET /data" in req:
            data = [{"foo": 1, "bar": 2.005}]
            data = json.dumps(data)
            ser.write(resp%("application/json",len(data),data))
        elif b"GET /" in req:
            with open("index.html") as index:
                data = index.read()
                ser.write(resp%("text/html",len(data),data))
    time.sleep(0.1)
