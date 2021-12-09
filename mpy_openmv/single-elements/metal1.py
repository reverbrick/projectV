import sensor, image, time, math, json
from pyb import Pin
from machine import UART
from comms import recv_msg, send_msg
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.SXGA)
sensor.set_auto_exposure(False, exposure_us = 162739)
sensor.set_auto_whitebal(False, (60, 60, 65))
sensor.set_auto_gain(False, gain_db = 15)
sensor.set_quality(100)
sensor.skip_frames(time = 2000)

pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
center = (639, 559)
threshold = (15, 255)
threshold2 = (236, 255)

min_area = 8000
max_area = 18000
ratio_antoni = 0.32
ser = UART(3, 115200)

#########################
show_rects = True
show_roi = False
show_six_points = False
show_threshold = False
#########################

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
pin0.value(1)

while(True):
    img = sensor.snapshot(). lens_corr(0.9)
    if show_threshold == True:
        img.binary([threshold])
    buf = recv_msg(ser)
    val = []
    for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):
        rect = b.rect()
        if b.pixels() > min_area and b.pixels() < max_area:
            l_a = b.major_axis_line()
            angle_a = math.atan2(l_a[1] - l_a[3], l_a[0] - l_a[2])
            if distance(b.cx(), b.cy(), l_a[0], l_a[1]) > distance(b.cx(), b.cy(), l_a[2], l_a[3]):
                angle_a = angle_a + math.radians(180)
            a1x = int(b.cx() - 5 * math.cos(angle_a))
            a1y = int(b.cy() - 5 * math.sin(angle_a))
            roi = (a1x-30, a1y-30, 60, 60)
            pix = []
            for b2 in img.find_blobs([threshold2], roi = roi, merge = True):
                pix.append(b2.pixels())
            if show_roi == True:
                img.draw_rectangle(roi, color=(255,255,255))
                #img.draw_string(b.cx(), b.cy(), "%s"%sum(pix), scale = 3)
                if distance(b.cx(), b.cy(), l_a[0], l_a[1]) > distance(b.cx(), b.cy(), l_a[2], l_a[3]):
                    img.draw_string(b.cx(),b.cy(),"%s"%round(distance(b.cx(), b.cy(), l_a[0], l_a[1])/distance(b.cx(), b.cy(), l_a[2], l_a[3]),2), (255,255,255), scale = 2)
                else:
                    img.draw_string(b.cx(), b.cy(), "%s"%round(distance(b.cx(), b.cy(), l_a[2], l_a[3])/distance(b.cx(), b.cy(), l_a[0], l_a[1]),2), (255,255,255), scale = 2)
            if sum(pix) >=0 and sum(pix) <= 8:
                l = b.major_axis_line()
                major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                ratio_minor = major_len/minor_len
                if (major_len > 385 and major_len < 410) and (ratio_minor > 7 and ratio_minor < 10):
                    angle = math.atan2(l[1] - l[3], l[0] - l[2])
                    if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + math.radians(180)
                    c1x = int(b.cx() - 100 * math.cos(angle))
                    c1y = int(b.cy() - 100 * math.sin(angle))
                    angle1 = angle
                    angle2 = angle
                    c3x = int(b.cx() - 40 * math.cos(angle1))
                    c3y = int(b.cy() - 40 * math.sin(angle1))
                    angle1 = angle1 + math.radians(90)
                    c4x = int(c3x - 50 * math.cos(angle1))
                    c4y = int(c3y - 50 * math.sin(angle1))
                    angle1 = angle1 + math.radians(90)
                    c5x = int(c4x - 40 * math.cos(angle1))
                    c5y = int(c4y - 40 * math.sin(angle1))
                    c6x = int(c5x - 40 * math.cos(angle1))
                    c6y = int(c5y - 40 * math.sin(angle1))
                    d3x = int(b.cx() - 40 * math.cos(angle2))
                    d3y = int(b.cy() - 40 * math.sin(angle2))
                    angle2 = angle2 - math.radians(90)
                    d4x = int(d3x - 50 * math.cos(angle2))
                    d4y = int(d3y - 50 * math.sin(angle2))
                    angle2 = angle2 - math.radians(90)
                    d5x = int(d4x - 40 * math.cos(angle2))
                    d5y = int(d4y - 40 * math.sin(angle2))
                    d6x = int(d5x - 40 * math.cos(angle2))
                    d6y = int(d5y - 40 * math.sin(angle2))
                    roi1 = (c4x-1, c4y-1, 2, 2)
                    roi2 = (c5x-1, c5y-1, 2, 2)
                    roi3 = (c6x-1, c6y-1, 2, 2)
                    roi4 = (d4x-1, d4y-1, 2, 2)
                    roi5 = (d5x-1, d5y-1, 2, 2)
                    roi6 = (d6x-1, d6y-1, 2, 2)
                    try:
                        stats1a = img.get_statistics(thresholds = [threshold], roi = roi1)
                        stats2a = img.get_statistics(thresholds = [threshold], roi = roi2)
                        stats3a = img.get_statistics(thresholds = [threshold], roi = roi3)
                        stats1b = img.get_statistics(thresholds = [threshold], roi = roi4)
                        stats2b = img.get_statistics(thresholds = [threshold], roi = roi5)
                        stats3b = img.get_statistics(thresholds = [threshold], roi = roi6)
                        if show_six_points == True:
                            img.draw_rectangle(roi1)
                            img.draw_rectangle(roi2)
                            img.draw_rectangle(roi3)
                            img.draw_rectangle(roi4)
                            img.draw_rectangle(roi5)
                            img.draw_rectangle(roi6)
                        if stats1a[0] == 0 and stats2a[0] == 0 and stats3a[0] == 0 and stats1b[0] == 0 and stats2b[0] == 0 and stats3b[0] == 0:
                            roi = (c1x-2, c1y-2, 4, 4)
                            stats = img.get_statistics(roi=roi, thresholds =[threshold])
                            if stats[0] == 0:
                                angle = round(angle, 2)
                                angle = math.degrees(angle)
                                if show_rects == True:
                                    img.draw_rectangle(b.rect(), color=(10,255,0), thickness= 2)
                                    img.draw_rectangle(rect[0], rect[1]-15, 80, 15, (10, 255, 0), fill=True)
                                    img.draw_string(rect[0], rect[1]-18, "Pick1", (0, 0, 0), scale = 2)
                                    img.draw_cross(b.cx(), b.cy(), (0,0,0) ,size=8, thickness = 3)
                                    img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (0, 255, 0), thickness = 3)
                                if angle > 180:
                                    angle = angle - 360
                                if major_len > minor_len:
                                    ratio = 124 / major_len
                                elif minor_len > major_len:
                                    ratio = 124 / minor_len
                                x = (b.cx() - center[0]) * ratio
                                y = (b.cy() - center[1]) * ratio
                                y = y * -1
                                angle = angle * -1
                                out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 1}
                                val.append(out)
                    except:
                        pass
            elif sum(pix) >= 100:
                l = b.major_axis_line()
                major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                ratio_minor = major_len/minor_len
                if (major_len > 380 and major_len < 410) and (ratio_minor > 7 and ratio_minor < 10):
                    angle = math.atan2(l[1] - l[3], l[0] - l[2])
                    if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + math.radians(180)
                    c1x = int(b.cx() - 100 * math.cos(angle))
                    c1y = int(b.cy() - 100 * math.sin(angle))
                    angle1 = angle
                    angle2 = angle
                    c3x = int(b.cx() - 40 * math.cos(angle1))
                    c3y = int(b.cy() - 40 * math.sin(angle1))
                    angle1 = angle1 + math.radians(90)
                    c4x = int(c3x - 50 * math.cos(angle1))
                    c4y = int(c3y - 50 * math.sin(angle1))
                    angle1 = angle1 + math.radians(90)
                    c5x = int(c4x - 40 * math.cos(angle1))
                    c5y = int(c4y - 40 * math.sin(angle1))
                    c6x = int(c5x - 40 * math.cos(angle1))
                    c6y = int(c5y - 40 * math.sin(angle1))
                    d3x = int(b.cx() - 40 * math.cos(angle2))
                    d3y = int(b.cy() - 40 * math.sin(angle2))
                    angle2 = angle2 - math.radians(90)
                    d4x = int(d3x - 50 * math.cos(angle2))
                    d4y = int(d3y - 50 * math.sin(angle2))
                    angle2 = angle2 - math.radians(90)
                    d5x = int(d4x - 40 * math.cos(angle2))
                    d5y = int(d4y - 40 * math.sin(angle2))
                    d6x = int(d5x - 40 * math.cos(angle2))
                    d6y = int(d5y - 40 * math.sin(angle2))
                    roi1 = (c4x-1, c4y-1, 2, 2)
                    roi2 = (c5x-1, c5y-1, 2, 2)
                    roi3 = (c6x-1, c6y-1, 2, 2)
                    roi4 = (d4x-1, d4y-1, 2, 2)
                    roi5 = (d5x-1, d5y-1, 2, 2)
                    roi6 = (d6x-1, d6y-1, 2, 2)
                    try:
                        stats1a = img.get_statistics(thresholds = [threshold], roi = roi1)
                        stats2a = img.get_statistics(thresholds = [threshold], roi = roi2)
                        stats3a = img.get_statistics(thresholds = [threshold], roi = roi3)
                        stats1b = img.get_statistics(thresholds = [threshold], roi = roi4)
                        stats2b = img.get_statistics(thresholds = [threshold], roi = roi5)
                        stats3b = img.get_statistics(thresholds = [threshold], roi = roi6)
                        if show_six_points == True:
                            img.draw_rectangle(roi1)
                            img.draw_rectangle(roi2)
                            img.draw_rectangle(roi3)
                            img.draw_rectangle(roi4)
                            img.draw_rectangle(roi5)
                            img.draw_rectangle(roi6)
                        if stats1a[0] == 0 and stats2a[0] == 0 and stats3a[0] == 0 and stats1b[0] == 0 and stats2b[0] == 0 and stats3b[0] == 0:
                            roi = (c1x-2, c1y-2, 4, 4)
                            stats = img.get_statistics(roi=roi, thresholds =[threshold])
                            if stats[0] == 0:
                                angle = round(angle, 2)
                                angle = math.degrees(angle)
                                if show_rects == True:
                                    img.draw_rectangle(b.rect(), color=(255,10,0), thickness= 2)
                                    img.draw_rectangle(rect[0], rect[1]-15, 80, 15, (255, 10, 0), fill=True)
                                    img.draw_string(rect[0], rect[1]-18, "Pick2", (0, 0, 0), scale = 2)
                                    img.draw_cross(b.cx(), b.cy(), (0,0,0) ,size=8, thickness = 3)
                                    img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (255, 10, 0), thickness = 3)
                                if angle > 180:
                                    angle = angle - 360
                                if major_len > minor_len:
                                    ratio = 124 / major_len
                                elif minor_len > major_len:
                                    ratio = 124 / minor_len

                                x = (b.cx() - center[0]) * ratio
                                y = (b.cy() - center[1]) * ratio
                                y = y * -1
                                angle = angle * -1
                                out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 2}
                                val.append(out)
                    except:
                        pass
    img.draw_circle(center[0], center[1], 4, (80,80,255), 2, False)
    if buf == b"snap":
        send_msg(ser,bytearray(json.dumps(val)))
    img.draw_string(20, 20, "Ilosc detali: %s"%len(val) + " Buf: %s"%buf, (255, 255, 255), scale = 2)
