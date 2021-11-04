from machine import UART
from ioia import Camera, Flash, Velux
import time, sensor, omv
import ubinascii, math, json
omv.disable_fb(True)
cam = Camera(exposure=54000, framesize="SXGA")
cam.sensor.set_quality(100)
cam.sensor.set_contrast(0)
cam.sensor.set_brightness(0)
fla = Flash(100,0)
ratio = 0.73
ser = UART(3, 921600)
resp = b"""HTTP/1.1 200 OK\r\nConnection: Close\r\nContent-type: %s\r\nContent-Length: %s\r\n\r\n%s\x0D"""
x=0
while(True):
	req = ser.readline()
	if req:
		if b"GET /data" in req:
			x=x+1
			data = [{"foo": x, "bar": 2.005}]
			data = json.dumps(data)
			ser.write(resp%("application/json",len(data),data))
		elif b"GET /img" in req:
			img = cam.snap(fla, corr=0.9)
			img = img.copy(x_size=640, copy_to_fb=True).compress(quality=50)
			data = ubinascii.a2b_base64((ubinascii.b2a_base64(img)))
			ser.write(resp%("image/jpeg",len(data),data))
		elif b"GET /roi" in req:
			img = cam.snap(fla, corr=0.9)
			img.draw_line(640,0,640,1024,color=(255,0,0),thickness=1)
			img.draw_line(0,512,1024,512,color=(255,0,0),thickness=1)
			img = img.copy(roi=(320,256,640,512), copy_to_fb=True).compress(quality=50)
			data = ubinascii.a2b_base64((ubinascii.b2a_base64(img)))
			ser.write(resp%("image/jpeg",len(data),data))
		elif b"GET /calib" in req:
			with open("index.html") as index:
				data = index.read()
				data = data.replace("/img","/roi")
				ser.write(resp%("text/html",len(data),data))
		elif b"GET /" in req:
			with open("index.html") as index:
				data = index.read()
				ser.write(resp%("text/html",len(data),data))
	time.sleep(0.1)