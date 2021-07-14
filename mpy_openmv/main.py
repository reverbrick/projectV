from machine import UART
from ioia import Camera, Flash, Velux; import time
cam = Camera(exposure=100)
fla = Flash(0,0)
cli = Velux()
ser = UART(3, 115200)
while(True):
	if ser.any():
		buf = ser.readline()
		img = cam.snap(fla)
		img.mask_circle([130,490,500])
		img.draw_circle([130,480,90], color=(0,0,0),fill=True)
		ret = cli.plastic(img,(109, 255),debug=True, close=4, ratio=0.625)
		ser.write(str(ret))
