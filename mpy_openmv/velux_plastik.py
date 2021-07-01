import sensor, image, time, math
from pyb import Pin

#params
delay = 0.8
threshold = (103, 255)
ratio=0.73
#ratio=1.35

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def blobs(img, threshold):
    ret = {}
    for b in img.find_blobs([(255,255)], pixels_threshold=2300, merge=False):
        if b.pixels()<4000:
            #print(b.pixels())
            #blob rotation
            l = b.major_axis_line()
            #angle from 2 points
            angle = math.atan2(l[1] - l[3], l[0] - l[2])
            #angle correction based on distance
            if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(),l[2],l[3]):
                angle = angle + math.radians(180)
            c2x = int(b.cx() + 80 * math.cos(angle))
            c2y = int(b.cy() + 80 * math.sin(angle))
            img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,0,0))
            img.draw_cross(b.cx(), b.cy(), color=(255,0,0))
            img.draw_line(b.major_axis_line(), color=(255,0,0))
            img.draw_line(b.minor_axis_line(), color=(255,0,0))
            ret['x']=b.cx()*ratio
            ret['y']=b.cy()*ratio
            angle = math.degrees(angle)
            if angle<0:
                angle=angle+360
            ret['angle']=angle
    return ret

#leds = leds()
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)

#camera
sensor.reset()
#todo check initialization for different expositions
#sensor.set_jb_quality(95)
sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_auto_exposure(False, exposure_us=4000)
#sensor.set_auto_exposure(True)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
sensor.set_contrast(0)
sensor.set_brightness(0)
sensor.skip_frames(20)

def get(threshold=threshold):
    ret={}
    start = time.ticks_ms()
    #leds.on()
    pin0.value(1)
    time.sleep(0.2)
    img = sensor.snapshot()
    time.sleep(0.1)
    pin0.value(0)
    img.draw_cross(320, 240, color=(255,255,255),thickness=1)
    #leds.off()
    if False:
        img.mask_circle([130,470,450])
        img.draw_circle([120,480,80], color=(0,0,0),fill=True)
        img.binary([threshold])
        img.close(3)
        ret = blobs(img, threshold)
    print(sensor.get_exposure_us())
    #print(sensor.get_gain_db())
    #print(sensor.get_rgb_gain_db())
    ret['time_us']=time.ticks_diff(time.ticks_ms(), start)
    print(ret)
    #print("--- %s seconds ---" % (time.time() - start))

while True:
    get()
    time.sleep(delay)
