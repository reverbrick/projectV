from machine import UART
from ioia import Camera, Flash, Velux; import time
from comms import recv_msg, send_msg
cam = Camera(exposure=50000, framesize="VGA")
fla = Flash(0.1,0)
cli = Velux()
ser = UART(3, 115200)
while(True):
    buf = recv_msg(ser)
    #if True:
    if buf==b"snap":
        img = cam.snap(fla, corr=0.9)
        h = img.get_histogram()
        t = h.get_threshold()[0]
        img.binary([(t,255)])
        img.erode(2)
        img.close(4)
        img.erode(2)
        #img.mask_circle([200,550,590])
        #img.draw_circle([130,480,90], color=(0,0,0),fill=True)
        ret = cli.plastic(img,(222, 255),debug=False, close=6, erode=6, min=2000, max=2500, ratio=0.625)
        send_msg(ser,bytearray(ret))
        #print(ret)
    time.sleep(0.1)
