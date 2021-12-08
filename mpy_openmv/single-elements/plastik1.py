# Untitled - By: dawid - pon. lis 29 3321

import sensor, image, time, math, json
from pyb import Pin
from machine import UART
from comms import recv_msg, send_msg

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.SXGA)
sensor.set_quality(100)
sensor.set_contrast(-3)
sensor.set_brightness(-3)
sensor.set_auto_whitebal(False, (60.2071, 61.0849, 66.9353))
sensor.set_auto_gain(False, gain_db = 6.0207)
sensor.set_auto_exposure(False, exposure_us = 74000)
sensor.skip_frames(time = 3300)

################################
# Call selected cells
show_rects = True
show_roi = False
show_threshold = False

################################
# Global variables
ser = UART(3, 115330)
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
center = (664, 561)
threshold = (8, 255)
ratio = 0.32


def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

pin0.value(1)
while(True):
    img = sensor.snapshot().lens_corr(0.9)
    img.draw_rectangle(0, 0, 300, 1024, (0, 0, 0), fill=True)
    buf = recv_msg(ser)
    if show_threshold == True:
        img.binary([threshold])
    val = []
    for b in img.find_blobs([threshold], merge=False, pixels_threshold=3800):
        ret = {}
        pix = b.pixels()
        if pix > 11000 and pix < 24300:
            #img.draw_string(b.cx(), b.cy(), "%s"%b.pixels(), color=(255,255,255), scale = 3)
            c = b.corners()
            #print(c)
            l = b.major_axis_line()
            k = b.minor_axis_line()
            angle = math.atan2(l[1] - l[3], l[0] - l[2])
            if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(),l[2],l[3]):
                angle = angle + math.radians(180)

            angle_out = angle
            angle2 = angle
            c2x = int(b.cx() + 33 * math.cos(angle))
            c2y = int(b.cy() + 33 * math.sin(angle))

            angle = math.atan2(k[1] - k[3], k[0] - k[2])
            if distance(b.cx(), b.cy(),k[0],k[1]) > distance(b.cx(), b.cy(),k[2],k[3]):
                angle = angle + math.radians(180)
            major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
            minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
            if major_len > 300 and major_len < 360:
                #img.draw_string(b.cx(), b.cy(),"%s"%major_len, scale = 3)
                c1x = int(c2x + 22 * math.cos(angle))
                c1y = int(c2y + 22 * math.sin(angle))

                angle1 = angle2 + math.radians(180)

                #            (center) - - b1x b1y
                b1x = int(c1x + 33 * math.cos(angle1))
                b1y = int(c1y + 33 * math.sin(angle1))

                angle1 = angle1 + math.radians(90)
                d1x = int(b1x + 42 * math.cos(angle1))
                d1y = int(b1y + 42 * math.sin(angle1))

                angle1 = angle1 - math.radians(180)
                d2x = int(b1x + 42 * math.cos(angle1))
                d2y = int(b1y + 42 * math.sin(angle1))

                angle1 = angle1 + math.radians(90)
                b2x = int(b1x + 33 * math.cos(angle1))
                b2y = int(b1y + 33 * math.sin(angle1))

                angle1 = angle1 + math.radians(90)
                b3x = int(b2x + 42 * math.cos(angle1))
                b3y = int(b2y + 42 * math.sin(angle1))

                angle1 = angle1 - math.radians(180)
                b4x = int(b2x + 42 * math.cos(angle1))
                b4y = int(b2y + 42 * math.sin(angle1))

                c4x = int(c1x + 42 * math.cos(angle))
                c4y = int(c1y + 42 * math.sin(angle))

                angle = angle + math.radians(180)
                c5x = int(c1x + 42 * math.cos(angle))
                c5y = int(c1y + 42 * math.sin(angle))

                # roi rects
                roi1 = (c4x-3, c4y-3, 6, 6)
                roi2 = (c5x-3, c5y-3, 6, 6)
                roi3 = (d1x-3, d1y-3, 6, 6)
                roi4 = (d2x-3, d2y-3, 6, 6)
                roi5 = (b3x-3, b3y-3, 6, 6)
                roi6 = (b4x-3, b4y-3, 6, 6)

                if show_roi == True:
                    img.draw_rectangle(c4x-3, c4y-3, 6, 6)
                    img.draw_rectangle(c5x-3, c5y-3, 6, 6)
                    img.draw_rectangle(d1x-3, d1y-3, 6, 6)
                    img.draw_rectangle(d2x-3, d2y-3, 6, 6)
                    img.draw_rectangle(b3x-3, b3y-3, 6, 6)
                    img.draw_rectangle(b4x-3, b4y-3, 6, 6)
                try:
                    stats1a = img.get_statistics(thresholds = [threshold], roi = roi1)
                    stats2a = img.get_statistics(thresholds = [threshold], roi = roi2)
                    stats3a = img.get_statistics(thresholds = [threshold], roi = roi3)
                    stats1b = img.get_statistics(thresholds = [threshold], roi = roi4)
                    stats2b = img.get_statistics(thresholds = [threshold], roi = roi5)
                    stats3b = img.get_statistics(thresholds = [threshold], roi = roi6)
                    if stats1a[0] == 0 and stats2a[0] == 0 and stats3a[0] == 0 and stats1b[0] == 0 and stats2b[0] == 0 and stats3b[0] == 0:
                        if show_rects == True:
                            img.draw_rectangle(b.rect(), color=(10, 255, 0), thickness = 2)
                            img.draw_rectangle(b.rect()[0], b.rect()[1]-15, 80, 15, (10, 255, 0), fill=True)
                            img.draw_string(b.rect()[0], b.rect()[1]-18, "Pick", (0, 0, 0), scale = 2)
                            #img.draw_cross(b1x, b1y, (255,255,0), 4, 2)
                            #img.draw_arrow(c1x,c1y,b1x,b1y, (255,255,0))

                        angle = math.degrees(angle_out)
                        angle = round(angle, 3)
                        if angle > 180:
                            angle = angle - 360
                        angle = angle * -1

                        #img.draw_string(b.cx(), b.cy(), "%s"%angle, scale= 3)
                        x = (b1x - center[0]) * ratio
                        y = (b1y - center[1]) * ratio
                        #img.draw_cross(b1x, b1y, (255,255,0), 4, 2)
                        y = y * -1
                        out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 1}

                        img.draw_cross(b1x, b1y, (255,255,0), 4, 2)
                        #print(out)
                        val.append(out)

                    else:
                        #img.draw_rectangle(bsend_ms.rect(), color=(10, 100, 0), thickness = 2)
                        img.draw_rectangle(b.rect()[0], b.rect()[1]-15, 80, 15, (10, 255, 0), fill=True)
                        img.draw_string(b.rect()[0], b.rect()[1]-18, "NOk", (0, 0, 0), scale = 2)
                except:
                    pass
    img.draw_circle(center[0], center[1], 1, (255,255,255), 2, False)
    if buf == b"snap":
        #print("Snap")
        #print(val)
        send_msg(ser,bytearray(json.dumps(val)))
