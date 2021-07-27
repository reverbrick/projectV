import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
#sensor.set_windowing((160, 120)) # Look at center 160x120 pixels of the VGA resolution.
sensor.skip_frames(time = 2000)
sensor.set_quality(100)

ratio=1.688

while(True):
    img = sensor.snapshot()
    #line = img.draw_line(220, 240, 420, 240, color = (255, 255, 255))
    center = (80,60)
    #img.binary([(107,255)],invert=True)
    #for c in img.find_circles(threshold=3000):
    #    print(c)
    #    img.draw_cross(c[0],c[1], color=(0,0,0),thickness=1)
    img.draw_cross(center, color=(0,0,0),thickness=1)
    for x in range(30):
        a = int(x*15*ratio)
        img.draw_line(a,0,a,480,color=(0,0,0),thickness=1)
        img.draw_line(0,a,640,a,color=(0,0,0),thickness=1)

