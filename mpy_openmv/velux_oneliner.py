from ioia import Camera, Flash, Velux; import time;cam = Camera(exposure=2000);fla = Flash(0.2,0.1);cli = Velux()

while(True):
    #cam.snap(fla)
    print(cli.plastic(cam.snap(fla),(125, 255),debug=True))
    time.sleep(1)
