##################
#
#     Plastik 2
#
##################
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
sensor.set_auto_exposure(False, exposure_us = 134000)
sensor.skip_frames(time = 3300)


ser = UART(3, 115200)
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
threshold = (49, 255)
ratio = 0.3190
center = (637, 530)

show_rois = True
show_rects = True


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

pin0.value(1)
while(True):

    img = sensor.snapshot().lens_corr(0.9)
    img.mask_circle(637, 1000, 850)
    val = []
    buf = recv_msg(ser)

    for b in img.find_blobs([threshold]):

        if b.pixels() > 7200 and b.pixels() < 9000:
            major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
            minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))

            if major_len != 0 and minor_len !=0:

                if major_len/minor_len > 4.8 and major_len/minor_len < 6:

                    if major_len > 310 and major_len < 340:

                            rect = b.rect()

                            l = b.major_axis_line()
                            angle = math.atan2(l[1] - l[3], l[0] - l[2])
                            angle = angle - math.radians(5)

                            c1x = int(b.cx() + 150 * math.cos(angle))
                            c1y = int(b.cy() + 150 * math.sin(angle))
                            roi = (c1x - 1, c1y - 1, 2, 2)
                            if roi[0] < 1250 and roi[1] < 1020:
                                stats = img.get_statistics(roi = roi, threholds = ([threshold]))

                                if stats[0] == 0:
                                    angle = angle - math.radians(170)
                                    c1x = int(b.cx() + 150 * math.cos(angle))
                                    c1y = int(b.cy() + 150 * math.sin(angle))

                                roi = (c1x-1, c1y-1, 2, 2)
                                if roi[0] < 1250 and roi[1] < 1020:
                                    stats = img.get_statistics(roi = roi, threholds = ([threshold]))
                                    if stats[0] != 0:
                                        angle_out = angle
                                        angle_check = angle
                                        angle1 = angle
                                        angle1 = angle1 + math.radians(90)
                                        a1x = int(b.cx() + 40 * math.cos(angle1))
                                        a1y = int(b.cy() + 40 * math.sin(angle1))
                                        angle1 = angle1 - math.radians(90)
                                        a2x = int(a1x + 30 * math.cos(angle1))
                                        a2y = int(a1y + 30 * math.sin(angle1))
                                        angle1 = angle1 - math.radians(180)
                                        a3x = int(a1x + 30 * math.cos(angle1))
                                        a3y = int(a1y + 30 * math.sin(angle1))
                                        angle1 = angle1 + math.radians(90)
                                        b2x = int(b.cx() + 40 * math.cos(angle1))
                                        b2y = int(b.cy() + 40 * math.sin(angle1))
                                        angle1 = angle1 - math.radians(90)
                                        b3x = int(b2x+ 30 * math.cos(angle1))
                                        b3y = int(b2y + 30 * math.sin(angle1))
                                        angle1 = angle1 + math.radians(180)
                                        b4x = int(b2x + 30 * math.cos(angle1))
                                        b4y = int(b2y + 30 * math.sin(angle1))

                                        roi1 = (a1x-2, a1y-2, 4, 4)
                                        roi2 = (a2x-2, a2y-2, 4, 4)
                                        roi3 = (a3x-2, a3y-2, 4, 4)
                                        roi4 = (b2x-2, b2y-2, 4, 4)
                                        roi5 = (b3x-2, b3y-2, 4, 4)
                                        roi6 = (b4x-2, b4y-2, 4, 4)

                                        try:
                                            stats1a = img.get_statistics(thresholds = [threshold], roi = roi1)
                                            stats2a = img.get_statistics(thresholds = [threshold], roi = roi2)
                                            stats3a = img.get_statistics(thresholds = [threshold], roi = roi3)
                                            stats1b = img.get_statistics(thresholds = [threshold], roi = roi4)
                                            stats2b = img.get_statistics(thresholds = [threshold], roi = roi5)
                                            stats3b = img.get_statistics(thresholds = [threshold], roi = roi6)

                                            if stats1a[0] == 0 and stats2a[0] == 0 and stats3a[0] == 0 and stats1b[0] == 0 and stats2b[0] == 0 and stats3b[0] == 0:

                                                d1x = int(b.cx() - 120 * math.cos(angle_check))
                                                d1y = int(b.cy() - 120 * math.sin(angle_check))
                                                angle_check = angle_check - math.radians(90)

                                                # check side here
                                                d2x = int(d1x + 25 * math.cos(angle_check))
                                                d2y = int(d1y + 25 * math.sin(angle_check))

                                                angle = math.degrees(angle_out)
                                                if angle > 180:
                                                    angle = angle - 360
                                                angle = angle * -1
                                                x = (b.cx() - center[0]) * ratio
                                                y = (b.cy() - center[1]) * ratio
                                                y = y * -1


                                                roi_side = (d2x-1, d2y-1, 2, 2)
                                                try:
                                                    stats_side = img.get_statistics(thresholds = [threshold], roi = roi_side)
                                                    if stats_side[0] < 10:
                                                        img.draw_rectangle(rect[0], rect[1] - 10,rect[2], 10, (255, 255, 255), fill=True)
                                                        img.draw_string(rect[0], rect[1]-10, "side1", (0, 0, 0))
                                                        out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 1}
                                                        val.append(out)
                                                    elif stats_side[0] > 80:
                                                        img.draw_rectangle(rect[0], rect[1] - 10,rect[2], 10, (255, 255, 255), fill=True)
                                                        img.draw_string(rect[0], rect[1]-10, "side2", (0, 0, 0))
                                                        out = {"x": round(x,3), "y": round(y,3), "angle": round(angle,3), "side": 2}
                                                        val.append(out)

                                                    if show_rects == True:
                                                        img.draw_arrow(b.cx(), b.cy(), c1x, c1y , thickness = 3)
                                                        img.draw_cross(b.cx(), b.cy(), 0, 10, 6)
                                                        img.draw_rectangle(rect, color = (0, 255, 0))
                                                    if show_rois == True:
                                                        img.draw_rectangle(roi1)
                                                        img.draw_rectangle(roi2)
                                                        img.draw_rectangle(roi3)
                                                        img.draw_rectangle(roi4)
                                                        img.draw_rectangle(roi5)
                                                        img.draw_rectangle(roi6)
                                                except:
                                                    pass
                                        except:
                                            pass

    img.draw_circle(center[0], center[1], 4, (255,255,255), 2, True)
    if buf == b"snap":
        send_msg(ser,bytearray(json.dumps(val)))
    img.draw_string(20, 20, "Ilosc detali: %s"%len(val) + " Buf: %s"%buf, (255, 255, 255), scale = 2)
