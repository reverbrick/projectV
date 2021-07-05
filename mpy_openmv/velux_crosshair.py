# Untitled - By: dawid - pon. lip 5 2021

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    # Linia 200 px
    line = img.draw_line(220, 240, 420, 240, color = (255, 255, 255))
    img.draw_cross(320, 240, color=(255,255,255),thickness=1)
    print(clock.fps())
