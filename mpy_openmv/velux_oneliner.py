from ioia import Camera, Flash, Velux; import time
cam = Camera(exposure=1)
fla = Flash(0,0.1)
cli = Velux()

while(True):
    img = cam.snap(fla)
    img.mask_circle([130,490,500])
    img.draw_circle([130,480,90], color=(0,0,0),fill=True)
    ret = cli.plastic(img,(179, 255),debug=True, close=4, ratio=0.625)
    print(ret)

    #img.draw_cross(320, 240, color=(255,255,255),thickness=1)
    #print(cli.plastic(cam.snap(fla),(183, 255),debug=True))
    time.sleep(1)
