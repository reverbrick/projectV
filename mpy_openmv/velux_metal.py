import sensor, image, time, math
from pyb import Pin


#camera
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
#sensor.set_auto_exposure(False, exposure_us=1)
#sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
#sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
#sensor.set_contrast(0)
#sensor.set_brightness(10)
sensor.skip_frames(20)


#params
delay = 0.8
threshold = (176, 255)
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
min_degree = 0
max_degree = 360
ratio = 0.73

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def arrow(b, img):
    l = b.major_axis_line()
    angle = math.atan2(l[1] - l[3], l[0] - l[2])
    if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
        angle = angle + math.radians(180)
    angle = angle + math.radians(180)
    c2x = int(b.cx() + 80 * math.cos(angle))
    c2y = int(b.cy() + 80 * math.sin(angle))
    img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(0, 255, 0))
    img.draw_cross(b.cx(), b.cy(), color=(0, 255, 0))

def find_correct(b, img):
    l = b.major_axis_line()
    angle = math.atan2(l[1] - l[3], l[0] - l[2])

    if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
        angle = angle + math.radians(180)
    angle = angle + math.radians(180)

    angle = angle + math.radians(90)
    c1x = int(b.cx() + 13 * math.cos(angle))
    c1y = int(b.cy() + 13 * math.sin(angle))
    #img.draw_arrow(b.cx(), b.cy(), c1x, c1y, color=(0,0,0))

    c2x = int(b.cx() - 13 * math.cos(angle))
    c2y = int(b.cy() - 13 * math.sin(angle))
    #img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(0,255,0))

    angle = angle - math.radians(90)
    c3x = int(c2x + 120 * math.cos(angle))
    c3y = int(c2y + 120 * math.sin(angle))
    #img.draw_arrow(c2x, c2y, c3x, c3y, color=(0,255,0))

    angle = math.degrees(angle)
    if angle < 0:
        angle = angle + 360
    if angle > 360:
        angle = angle - 360
    angle = angle - 180

    roi = c3x - 5, c3y - 5, 10, 10
    try:
        roi = img.get_statistics(thresholds = [threshold], roi = roi)
    except OSError:
        pass
    if roi[0] == 0:
        img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "Correct position", (255, 255, 255))
        img.draw_string(int(b.cxf() + 5), int(b.cyf() + 50), "X:%s "%int(b.cxf())+"Y:%s "%int(b.cyf())+"an:%s "%int(angle), (0,255,0))
        img.draw_rectangle(b[0:4], color=(255, 255, 255))
        arrow(b,img)
    else:
        img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "Incorrect position", (255,0,0))

    #img.draw_circle(c3x, c3y, 3, (255,0,0), thickness = 2, fill = True)
    return angle

def translation(b ,img):
    #        w    h
    shape = 800, 600
    center = shape[0]/2, shape[1]/2
    print()

    # Oś X
    od_x = (b.cxf() - center[0]) * ratio

    # Oś Y
    od_y = (b.cyf() - center[1]) * ratio

    angle = find_correct(b, img)

    coords = (od_x, od_y, angle)

    return(coords)

def main(img, threshold):
    blob = img.find_blobs([threshold], pixels_threshold = 100, area_threshold = 4000)
    for b in blob:

        find_correct(b, img)

        translation(b, img)

        coords = translation(b, img)

        print(coords)

def get(threshold = threshold):
    start = time.ticks_ms()
    #pin0.value(1)
    #time.sleep(0.01)
    img = sensor.snapshot()
    img.draw_circle((630, 185, 90),(0, 0, 0), fill = True)
    #img.binary([threshold])

    main(img, threshold)

    #time.sleep(0.2)
    #pin0.value(0)


while True:
    get()
    #time.sleep(delay)
