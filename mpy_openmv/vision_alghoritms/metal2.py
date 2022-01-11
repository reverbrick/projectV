import sensor, image, time, math, json
from pyb import Pin
from machine import UART
from comms import recv_msg, send_msg

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.SXGA)
sensor.set_auto_exposure(False, exposure_us = 102739)
sensor.set_auto_whitebal(False, (60, 60, 65))
sensor.set_auto_gain(False, gain_db = 8)
sensor.set_quality(100)
sensor.skip_frames(time = 2000)
#########################
#
show_rects = True
show_six_points = False
#
#########################
threshold = (18, 255)
ser = UART(3, 115200)
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
ratio = 0.3190
center = (652, 505)

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
pin0.value(1)

while(True):
    img = sensor.snapshot()
    buf = recv_msg(ser)
    if buf == b"snap":
        img.binary([threshold])
        img.close(3)

        val = []
        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):

            if b.pixels() > 12500 and b.pixels() < 15500:

                major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                if major_len != 0 and major_len != 0:
                    if major_len/minor_len > 7 and major_len/minor_len < 9.8:

                        if major_len > 360 and major_len < 390:
                            rect = b.rect()
                            l = b.major_axis_line()
                            angle = math.atan2(l[1] - l[3], l[0] - l[2])
                            if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                                angle = angle + math.radians(180)

                            angle = angle + math.radians(180)

                            angle_out = angle

                            c1x = int(b.cx() + 100 * math.cos(angle))
                            c1y = int(b.cy() + 100 * math.sin(angle))
                            angle = angle - math.radians(270)
                            c2x = int(b.cx() - 15 * math.cos(angle))
                            c2y = int(b.cy() - 15 * math.sin(angle))
                            c2x_a = int(b.cx() + 15 * math.cos(angle))
                            c2y_a = int(b.cy() + 15 * math.sin(angle))
                            angle = angle + math.radians(270)
                            c3x = int(c2x + 180 * math.cos(angle))
                            c3y = int(c2y + 180 * math.sin(angle))
                            c3x_a = int(c2x_a + 180 * math.cos(angle))
                            c3y_a = int(c2y_a + 180 * math.sin(angle))
                            c3x = int(c2x + 180 * math.cos(angle))
                            c3y = int(c2y + 180 * math.sin(angle))

                            roi1 = (c3x-2, c3y-2, 4, 4)
                            roi2 = (c3x_a-2, c3y_a-2, 4, 4)

                            angle = angle + math.radians(90)
                            a1x = int(b.cx() + 50 * math.cos(angle))
                            a1y = int(b.cy() + 50 * math.sin(angle))
                            angle = angle - math.radians(180)
                            a2x = int(b.cx() + 50 * math.cos(angle))
                            a2y = int(b.cy() + 50 * math.sin(angle))
                            angle = angle + math.radians(90)
                            a3x = int(a2x + 30 * math.cos(angle))
                            a3y = int(a2y + 30 * math.sin(angle))
                            a4x = int(a2x - 30 * math.cos(angle))
                            a4y = int(a2y - 30 * math.sin(angle))
                            a5x = int(a1x + 30 * math.cos(angle))
                            a5y = int(a1y + 30 * math.sin(angle))
                            a6x = int(a1x - 30 * math.cos(angle))
                            a6y = int(a1y - 30 * math.sin(angle))

                            roi1a = (a1x-2, a1y-2, 4, 4)
                            roi2a = (a2x-2, a2y-2, 4, 4)
                            roi3a = (a3x-2, a3y-2, 4, 4)
                            roi4a = (a4x-2, a4y-2, 4, 4)
                            roi5a = (a5x-2, a5y-2, 4, 4)
                            roi6a = (a6x-2, a6y-2, 4, 4)

                            try:
                                stats1a = img.get_statistics(thresholds = [threshold], roi = roi1a)
                                stats2a = img.get_statistics(thresholds = [threshold], roi = roi2a)
                                stats3a = img.get_statistics(thresholds = [threshold], roi = roi3a)
                                stats1b = img.get_statistics(thresholds = [threshold], roi = roi4a)
                                stats2b = img.get_statistics(thresholds = [threshold], roi = roi5a)
                                stats3b = img.get_statistics(thresholds = [threshold], roi = roi6a)
                                if stats1a[0] == 0 and stats2a[0] == 0 and stats3a[0] == 0 and stats1b[0] == 0 and stats2b[0] == 0 and stats3b[0] == 0:
                                    try:
                                        stats1 = img.get_statistics(roi=roi1, thresholds=[threshold])
                                        stats2 = img.get_statistics(roi=roi2, thresholds=[threshold])
                                        angle = math.degrees(angle_out)
                                        if show_six_points == True:
                                            img.draw_rectangle(roi1a)
                                            img.draw_rectangle(roi2a)
                                            img.draw_rectangle(roi3a)
                                            img.draw_rectangle(roi4a)
                                            img.draw_rectangle(roi5a)
                                            img.draw_rectangle(roi6a)
                                        if stats1[0] == 0 and stats2[0] == 255:
                                            if angle > 180:
                                                angle = angle - 360
                                            angle = angle * -1
                                            x = (b.cx() - center[0]) * ratio
                                            y = (b.cy() - center[1]) * ratio
                                            y = y * -1

                                            out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 1}
                                            val.append(out)
                                            if show_rects == True:
                                                img.draw_rectangle(b.rect(), color=(10,255,0), thickness= 2)
                                                img.draw_rectangle(rect[0], rect[1]-15, 80, 15, (10, 255, 0), fill=True)
                                                img.draw_string(rect[0], rect[1]-18, "side1", (0, 0, 0), scale = 2)
                                                img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (0, 255, 0), thickness = 3)
                                                img.draw_cross(b.cx(), b.cy(), (0,180,0), 8, 3)
                                        if stats2[0] == 0 and stats1[0] == 255:
                                            if angle > 180:
                                                angle = angle - 360
                                            angle = angle * -1
                                            x = (b.cx() - center[0]) * ratio
                                            y = (b.cy() - center[1]) * ratio
                                            y = y * -1

                                            out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 2}
                                            val.append(out)

                                            if show_rects == True:
                                                img.draw_rectangle(b.rect(), color=(10,255,0), thickness= 2)
                                                img.draw_rectangle(rect[0], rect[1]-15, 80, 15, (10, 255, 0), fill=True)
                                                img.draw_string(rect[0], rect[1]-18, "side2", (0, 0, 0), scale = 2)
                                                img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (0, 255, 0), thickness = 3)
                                                img.draw_cross(b.cx(), b.cy(), (0,180,0), 8, 3)

                                    except:
                                        pass
                            except:
                                pass
        print(val)
        img.draw_circle(center[0], center[1], 3, (0,255,0), 2, True)
        send_msg(ser,bytearray(json.dumps(val)))
        img.draw_string(20, 20, "Ilosc detali: %s"%len(val) + " Buf: %s"%buf, (255, 255, 255), scale = 2)
