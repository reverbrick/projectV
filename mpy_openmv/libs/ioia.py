ratio=0.73

class Camera():
    import sensor

    def __init__(self, pixformat="GRAYSCALE", exposure=0, framesize="SVGA", contrast=0, brightness=0):
        self.sensor.reset()
        if pixformat=="GRAYSCALE":
            self.sensor.set_pixformat(self.sensor.GRAYSCALE)
        else:
            self.sensor.set_pixformat(self.sensor.RGB565)
        if framesize=="QVGA":
            self.sensor.set_framesize(self.sensor.QVGA)
        elif framesize=="WQXGA2":
            self.sensor.set_framesize(self.sensor.WQXGA2)
        elif framesize=="QQVGA":
            self.sensor.set_framesize(self.sensor.QQVGA)
        elif framesize=="VGA":
            self.sensor.set_framesize(self.sensor.VGA)
        elif framesize=="SXGA":
            self.sensor.set_framesize(self.sensor.SXGA)
        elif framesize=="SVGA":
            self.sensor.set_framesize(self.sensor.SVGA)
        elif framesize=="HD":
            self.sensor.set_framesize(self.sensor.HD)
        else:
            self.sensor.set_framesize(self.sensor.VGA)
        if exposure == 0:
            self.sensor.set_auto_exposure(True)
        else:
            self.sensor.set_auto_exposure(False, exposure_us=exposure)
        self.sensor.set_contrast(contrast)
        self.sensor.set_brightness(brightness)
        self.sensor.skip_frames(time = 2000)
        self.sensor.set_auto_gain(False)
        self.sensor.set_auto_whitebal(False)

    def snap(self, flash = None, corr=0):
        if flash:
            flash.on()
        if corr == 0:
            img = self.sensor.snapshot()
        else:
            img = self.sensor.snapshot().lens_corr(strength=corr)
        if flash:
            flash.off()
        return img

class Flash():
    from pyb import Pin
    import time
    pre = 0
    post = 0
    def __init__(self, pre=0, post=0):
        self.pre = pre
        self.post = post
        self.pin = self.Pin('P0', self.Pin.OUT_PP, self.Pin.PULL_NONE)

    def on(self):
        self.pin.value(1)
        self.time.sleep_ms(self.pre)

    def off(self):
        self.time.sleep_ms(self.post)
        self.pin.value(0)

class Project_V():
    import math, json
    def distance(self, x1, y1, x2, y2):
        return self.math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def plastic1(self, img, threshold=(28, 86, 9, 86, -2, 64), close=0, ratio = 0.73, min_area = 3000, max_area = 7000, recive_coords = False):
        out = []

        for b in img.find_blobs([threshold], merge=False, pixels_threshold=3800):
            ret = {}

            if b.pixels() > min_area and b.pixels() < max_area:

                c = b.corners()
                l = b.major_axis_line()
                angle = self.math.atan2(l[1] - l[3], l[0] - l[2])

                if self.distance(b.cx(), b.cy(), l[0], l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
                    angle = angle + self.math.radians(180)
                    mmratio = self.distance(b.cx(), b.cy(), l[0], l[1]) / self.distance(b.cx(), b.cy(), l[2], l[3])

                else:
                    mmratio = self.distance(b.cx(), b.cy(), l[2], l[3]) / self.distance(b.cx(), b.cy(), l[0], l[1])

                if mmratio>1.3 and mmratio<1.7:
                    angle = angle + self.math.radians(180)
                    c2x = int(b.cx() + 80 * self.math.cos(angle))
                    c2y = int(b.cy() + 80 * self.math.sin(angle))

                    major_len = self.math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                    minor_len = self.math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))

                    if major_len / minor_len > 1.72 and major_len / minor_len < 2.1:
                        rect = b.rect()
                        angle = self.math.degrees(angle)

                        if angle < 0:
                            angle = angle + 360

                        if angle > 180:
                            angle = angle - 360

                        if recive_coords == True:
                            img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio, 5)+" mm")
                            img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio, 5)+" mm")
                            img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")

                        img.draw_rectangle(rect[0], rect[1]-10, rect[2], 10, (255, 255, 255), fill=True)
                        img.draw_rectangle(rect)
                        img.draw_string(rect[0], rect[1]-10, "Pick position", (0, 0, 0))
                        img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255, 255, 255), thickness = 3)
                        img.draw_cross(b.cx(), b.cy(), color=(255, 255, 255), size = 5, thickness = 3)

                        ret['x']=round((b.cx()-c_point[0])*ratio, 5)
                        ret['y']=round((b.cy()-c_point[1])*ratio, 5)
                        ret['angle']=round(angle, 5)

                out.append(ret)
        return self.json.dumps(out)

    def metal1(self, img, threshold=(4, 100, -6, 65, -39, 49), close=0, ratio = 0.73, min_area = 3200, max_area = 5000, recive_coords = False):
        out = []

        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):
            ret ={}

            if b.pixels() > min_area and b.pixels() < max_area:
                rect = b.rect()
                l = b.major_axis_line()
                roi = (b.cx()-5, b.cy()-5, 10, 10)
                major_len = self.math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = self.math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                stats = img.get_statistics(roi=roi)

                # Uncoment if something went wrong for get each parameter
                #img.draw_string(b.cx()-5, b.cy()-15, "%s"%stats[0]+ " %s"%stats[1], scale = 1)
                #img.draw_string(b.cx(), b.cy(), "%s"%(major_len/minor_len))
                #img.draw_string(b.cx(), b.cy(), "%s"%b.pixels())
                #img.draw_recangle(roi)

                if stats[0] >= 28:

                    if major_len/minor_len > 9 and major_len/minor_len < 12:

                        angle = self.math.atan2(l[1] - l[3], l[0] - l[2])
                        if self.distnace(b.cx(), b.cy(), l[0], l[1]) > self.distnace(b.cx(), b.cy(), l[2], l[3]):
                            angle = angle + self.math.radians(180)

                        c2x = int(b.cx() - 100 * self.math.cos(angle))
                        c2y = int(b.cy() - 100 * self.math.sin(angle))
                        angle = self.math.degrees(angle)
                        if angle < 0:
                            angle=angle + 180

                        if angle > 180:
                            angle=angle - 180

                        img.draw_arrow(b.cx(), b.cy(), c2x, c2y, (255, 255, 255), 4)
                        img.draw_cross(b.cx(), b.cy(), (0, 255, 0), size = 10, thickness = 3)
                        img.draw_rectangle(b.rect(), color= (0, 255, 0))
                        img.draw_rectangle(rect[0], rect[1]-10, rect[2], 10, (0, 255, 0), fill=True)
                        img.draw_string(rect[0], rect[1]-10, "Top position", (0, 0, 0))

                        if recive_coords == True:
                            img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio, 5)+" mm")
                            img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio, 5)+" mm")
                            img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")

                        ret['x']=round((b.cx()-c_point[0])*ratio, 5)
                        ret['y']=round((b.cy()-c_point[1])*ratio, 5)
                        ret['angle']=round(angle, 5)

                else:
                    angle = self.math.atan2(l[1] - l[3], l[0] - l[2])
                    if self.distnace(b.cx(), b.cy(), l[0], l[1]) > self.distnace(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + self.math.radians(180)

                    angle = angle + self.math.radians(270)
                    c2x = int(b.cx() - 10 * self.math.cos(angle))
                    c2y = int(b.cy() - 10 * self.math.sin(angle))

                    angle = angle - self.math.radians(90)
                    c3x = int(c2x + 115 * self.math.cos(angle))
                    c3y = int(c2y + 115 * self.math.sin(angle))

                    angle = self.math.degrees(angle)
                    if angle < 0:
                        angle=angle-360

                    if angle > 180:
                        angle=angle-360

                    roi = (c3x - 2, c3y - 2, 4, 4)

                    #Uncoment if you cant detect roi of right side element
                    #img.draw_rectangle(roi)

                    try:
                        stats = img.get_statistics(thresholds=([threshold]), roi= roi)

                        if stats[0] == 0:

                            img.draw_cross(b.cx(), b.cy(), (0, 0, 255), size = 10, thickness = 3)
                            img.draw_arrow(c2x, c2y, c3x, c3y)
                            img.draw_rectangle(b.rect(), color= (0, 0, 255))
                            img.draw_rectangle(rect[0], rect[1]-10, rect[2], 10, (0, 0, 255), fill=True)
                            img.draw_string(rect[0], rect[1]-10, "Right position", (0, 0, 0))

                            if recive_coords == True:
                                img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio, 5)+" mm")
                                img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio, 5)+" mm")
                                img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")

                            ret['x']=round((b.cx()-c_point[0])*ratio, 5)
                            ret['y']=round((b.cy()-c_point[1])*ratio, 5)
                            ret['angle']=round(angle, 5)
                    except:
                        pass
                out.append(ret)
        return self.json.dumps(out)

    def metal2(self, img, threshold = (14, 255), close=0, ratio = 0.73, min_area = 3000, max_area = 5900):

        if close !=0:
            img.binary([threshold])
            img.close(close)
        sub = {}
        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000, recive_coords = False):
            ret = {}
            if b.pixels() > min_area and b.pixels() < max_area:
                major_len = self.math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = self.math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                if major_len/minor_len > 7 and major_len/minor_len < 9:
                    l = b.major_axis_line()
                    angle = self.math.atan2(l[1] - l[3], l[0] - l[2])
                    if self.distnace(b.cx(), b.cy(), l[0], l[1]) > self.distnace(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + self.math.radians(180)

                    angle = angle + self.math.radians(180)
                    c1x = int(b.cx() + 100 * self.math.cos(angle))
                    c1y = int(b.cy() + 100 * self.math.sin(angle))

                    angle = angle - self.math.radians(270)
                    c2x = int(b.cx() - 8 * self.math.cos(angle))
                    c2y = int(b.cy() - 8 * self.math.sin(angle))

                    angle = angle + self.math.radians(270)
                    c3x = int(c2x + 112 * self.math.cos(angle))
                    c3y = int(c2y + 112 * self.math.sin(angle))
                    roi = (c3x-2, c3y-2, 4, 4)

                    try:
                        stats = img.get_statistics(roi=roi, thresholds=[threshold])
                        rect = b.rect()
                        if stats[0] == 0:
                            img.draw_rectangle(b.rect(), color= (0, 255, 0))
                            angle = self.math.degrees(angle)

                            if angle > 180:
                                angle = angle - 360

                            # Uncoment if something went wrong
                            #img.draw_string(b.cx(), b.cy(), "%s"%angle)
                            #img.draw_rectangle(roi)

                            img.draw_rectangle(rect[0], rect[1]-10, rect[2], 10, (0, 255, 0), fill=True)
                            img.draw_rectangle(b.rect(), color=(0, 255, 0))
                            img.draw_string(rect[0], rect[1]-10, "Pick position", (255, 255, 255))

                            if recive_coords == True:
                                img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx() - c_point[0]) * ratio, 5) + " mm")
                                img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy() - c_point[1]) * ratio, 5) + " mm")
                                img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")

                            img.draw_cross(b.cx(), b.cy(), (255, 255, 255), 8, 2)
                            img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (255, 255, 255), 2)

                            ret['x']=round((b.cx()-c_point[0])*ratio, 5)
                            ret['y']=round((b.cy()-c_point[1])*ratio, 5)
                            ret['angle']=round(angle, 5)

                    except:
                        pass
                out.append(ret)
        return self.json.dumps(out)

    def plastic2(self, img, threshold = (94, 255), close = 0, ratio = 0.73, min_area = 2700, max_area = 2900):
        out = []
        if close != 0:
            img.binary([threshold])
            img.close(close)
        sub = {}

        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000, recive_coords = False):
            ret = {}
            major_len = self.math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
            minor_len = self.math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))

            # Uncoment if something went wrong
            #img.draw_string(b.cx(), b.cy(), "%s"%b.pixels())
            #img.draw_string(b.cx(), b.cy(), "%s"%(major_len/minor_len))

            if major_len/minor_len > 4 and major_len/minor_len < 6:

                if b.pixels() > min_area and b.pixels() < max_area:
                    l = b.major_axis_line()
                    angle = self.math.atan2(l[1] - l[3], l[0] - l[2])

                    if self.distance(b.cx(), b.cy(), l[0], l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + self.math.radians(180)
                        angle = angle + self.math.radians(5)
                        c1x = int(b.cx() + 92 * self.math.cos(angle))
                        c1y = int(b.cy() + 92 * self.math.sin(angle))

                    else:

                        angle = angle - self.math.radians(5)
                        c1x = int(b.cx() + 92 * self.math.cos(angle))
                        c1y = int(b.cy() + 92 * self.math.sin(angle))
                    angle = self.math.degrees(angle)

                    if angle > 180:
                        angle = angle - 360

                    roi = (c1x - 1, c1y - 1, 1, 1)

                    try:
                        stats = img.get_statistics(roi = roi)

                        if stats[0] != 0:
                            # Uncoment if something went wrong
                            #img.draw_rectangle(roi)
                            rect = b.rect()
                            img.draw_rectangle(rect, color = (0, 255, 0))
                            img.draw_rectangle(rect[0], rect[1] - 10, rect[2], 10, (255, 255, 255), fill=True)
                            img.draw_string(rect[0], rect[1]-10, "Pick position", (0, 0, 0))

                            if recive_coords == True:
                                img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx() - c_point[0]) * ratio, 5) + " mm")
                                img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy() - c_point[1]) * ratio, 5) + " mm")
                                img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")

                            img.draw_cross(b.cx(), b.cy(), (255, 255, 255), 6, 3)
                            img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (255, 255, 255), 4)

                            ret['x']=round((b.cx()-c_point[0])*ratio, 5)
                            ret['y']=round((b.cy()-c_point[1])*ratio, 5)
                            ret['angle']=round(angle, 5)

                    except:
                        pass

                    out.append(ret)
        return self.json.dumps(out)
