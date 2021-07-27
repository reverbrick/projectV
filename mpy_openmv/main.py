from machine import UART
from ioia import Camera, Flash, Velux; import time
cam = Camera(exposure=300)
fla = Flash(0,0)
cli = Velux()
ser = UART(3, 115200)
while(True):
    if ser.any():
    #if True:
        buf = ser.readline()
        img = cam.snap(fla)
        img.mask_circle([200,550,590])
        #img.draw_circle([130,480,90], color=(0,0,0),fill=True)
        ret = cli.plastic(img,(147, 255),debug=False, close=3, erode=3, min=3500, max=5500, ratio=0.625)
        ser.write(str(ret))
    #time.sleep(0.4)
