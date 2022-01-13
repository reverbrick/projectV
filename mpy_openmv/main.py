from machine import UART
from ioia import Camera, Flash, Project_V; import time
from comms import recv_msg, send_msg
cam = Camera(exposure=50000, framesize="SVGA")
cam.sensor.set_quality(100)
fla = Flash(0.1,0)
cli = Project_V()
ser = UART(3, 115200)
while(True):
    buf = recv_msg(ser)
    #if True:
    if buf==b"snap":
        img = cam.snap(fla, corr=0.9)
        #img.mask_circle([230,500,590])
        #img.draw_circle([130,530,100], color=(0,0,0),fill=True)
        h = img.get_histogram()
        t = h.get_threshold()[0]
        img.binary([(t,255)])
        img.erode(2)
        img.close(6)
        #img.erode(2)
        ret = cli.plastic(img,(222, 255),debug=False, close=6, erode=6, min=3800, max=5500, ratio=0.625)
        send_msg(ser,bytearray(ret))
        print(ret)
    time.sleep(0.1)
