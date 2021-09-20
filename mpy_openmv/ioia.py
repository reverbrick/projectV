ratio=0.73
#ratio=1.35

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
        elif framesize=="QQVGA":
            self.sensor.set_framesize(self.sensor.QQVGA)
        elif framesize=="VGA":
            self.sensor.set_framesize(self.sensor.VGA)
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

class Velux():
    import math, json
    def distance(self,x1,y1,x2,y2):
        return self.math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def plastic(self, img, threshold=(103, 255), close=0, erode=0, dilate=0, min=2300, max=4000, debug=False, ratio=0.73):
        out = []
        #img.mask_circle([130,470,450])
        #img.draw_circle([120,480,80], color=(0,0,0),fill=True)
        """
        img.binary([threshold])
        if close!=0:
            img.close(close)
        else:
            if dilate!=0:
                img.dilate(dilate)
            if erode!=0:
                img.erode(erode)
        """
        for b in img.find_blobs([(255,255)], pixels_threshold=min, merge=False):
            pix = b.pixels()
            if pix<max:
                ret = {}
                #print(b.pixels())
                #blob rotation
                l = b.major_axis_line()
                #angle from 2 points
                angle = self.math.atan2(l[1] - l[3], l[0] - l[2])
                #angle correction based on distance
                if self.distance(b.cx(), b.cy(),l[0],l[1]) > self.distance(b.cx(), b.cy(),l[2],l[3]):
                    angle = angle + self.math.radians(180)
                c2x = int(b.cx() + 80 * self.math.cos(angle))
                c2y = int(b.cy() + 80 * self.self.math.sin(angle))
                img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,0,0))
                img.draw_cross(b.cx(), b.cy(), color=(255,0,0))
                img.draw_line(b.major_axis_line(), color=(255,0,0))
                img.draw_line(b.minor_axis_line(), color=(255,0,0))
                c_point = (320,240)
                ret['x']=round((b.cx()-c_point[0])*ratio,5)
                ret['y']=round((b.cy()-c_point[1])*ratio,5)
                ret['pix'] = pix
                angle = self.self.math.degrees(angle)
                #if angle<0:
                #    angle=angle+360
                if angle>180:
                    angle=angle-360
                ret['angle']=round(angle,5)
                out.append(ret)
        return self.json.dumps(out)

    def metal(self, img, threshold=(176, 255), ratio = 0.73):
        sub = {}
        for b in img.find_blobs([threshold], pixels_threshold = 100, area_threshold = 4000):
            l = b.major_axis_line()
            angle = self.self.math.atan2(l[1] - l[3], l[0] - l[2])
            if self.distance(b.cx(), b.cy(),l[0],l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
                angle = angle + self.self.math.radians(180)
            angle = angle + self.self.math.radians(180)

            angle = angle + self.self.math.radians(90)
            c1x = int(b.cx() + 13 * self.self.math.cos(angle))
            c1y = int(b.cy() + 13 * self.self.math.sin(angle))
            #img.draw_arrow(b.cx(), b.cy(), c1x, c1y, color=(0,0,0))

            c2x = int(b.cx() - 13 * self.self.math.cos(angle))
            c2y = int(b.cy() - 13 * self.self.math.sin(angle))
            #img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(0,255,0))

            angle = angle - self.self.math.radians(90)
            c3x = int(c2x + 120 * self.self.math.cos(angle))
            c3y = int(c2y + 120 * self.self.math.sin(angle))
            #img.draw_arrow(c2x, c2y, c3x, c3y, color=(0,255,0))

            roi = c3x - 5, c3y - 5, 10, 10
            try:
                roi = img.get_statistics(thresholds = [threshold], roi = roi)
            except OSError:
                pass

            if roi[0] == 0:
                img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "Correct position", (255, 255, 255))
                img.draw_string(int(b.cxf() + 5), int(b.cyf() + 50), "X:%s "%int(b.cxf())+"Y:%s "%int(b.cyf())+"an:%s "%int(angle), (0,255,0))
                img.draw_rectangle(b[0:4], color=(255, 255, 255))
                l = b.major_axis_line()
                angle = self.self.math.atan2(l[1] - l[3], l[0] - l[2])
                if self.distance(b.cx(), b.cy(), l[0], l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
                    angle = angle + self.self.math.radians(180)
                angle = angle + self.self.math.radians(180)
                c2x = int(b.cx() + 80 * self.self.math.cos(angle))
                c2y = int(b.cy() + 80 * self.self.math.sin(angle))
                img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(0, 255, 0))
                img.draw_cross(b.cx(), b.cy(), color=(0, 255, 0))
            else:
                img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "Incorrect position", (255,0,0))

                #img.draw_circle(c3x, c3y, 3, (255,0,0), thickness = 2, fill = True)
            angle = self.self.math.degrees(angle)
            if angle < 0:
                angle = angle + 360
            if angle > 360:
                angle = angle - 360
            angle = angle - 180
            #        w    h
            shape = 800, 600
            center = shape[0]/2, shape[1]/2

            # Oś X
            od_x = (b.cxf() - center[0]) * ratio

            # Oś Y
            od_y = (b.cyf() - center[1]) * ratio


            sub['x']=od_x
            sub['y']=od_y
            sub['angle']=angle
        return sub

    def metal2(self, img, threshold=(176, 255), close=2, ratio = 0.73, min_area= 5000, max_area=50000):
        img.binary([threshold])
        if close !=0:
            img.close(close)
        sub = {}
        for b in img.find_blobs([threshold], pixels_threshold = 100, area_threshold = 4000):
            if b.area() > min_area and b.area() < max_area:
                l = b.major_axis_line()
                angle = self.self.math.atan2(l[1] - l[3], l[0] - l[2])
                if self.distance(b.cx(), b.cy(), l[0], l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
                    angle = angle + self.self.math.radians(180)

                angle = angle - self.self.math.radians(90)
                c2x = int(b.cx() + 8 * self.self.math.cos(angle))
                c2y = int(b.cy() + 8 * self.self.math.sin(angle))

                angle = angle + self.self.math.radians(270)
                c3x = int(c2x + 124 * self.math.cos(angle))
                c3y = int(c2y + 124 * self.math.sin(angle))

                angle = self.math.degrees(angle)
                if angle < 0:
                    angle = angle + 360
                if angle > 360:
                    angle = angle - 360
                angle = angle - 180

                roi = c3x - 1, c3y - 1, 1, 1

                try:
                    roi = img.get_statistics(thresholds = [threshold], roi = roi)[0]
                except OSError:
                    pass

                if roi == 0:
                    img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "Correct position", (255, 255, 255))
                    img.draw_string(int(b.cxf() + 5), int(b.cyf() + 50), "X:%s "%int(b.cxf())+"Y:%s "%int(b.cyf())+"an:%s "%int(angle), (0,255,0), scale = 2)
                    img.draw_rectangle(b[0:4], color=(255, 255, 255))
                    img.draw_string(int(b.cxf() + 20), int(b.cyf() + 20), "%s"%roi, (255,0,0), scale = 2)
                    #        w    h
                    shape = 800, 600
                    center = shape[0]/2, shape[1]/2

                    # Oś X
                    od_x = (b.cxf() - center[0]) * ratio

                    # Oś Y
                    od_y = (b.cyf() - center[1]) * ratio

                    sub['x']=od_x
                    sub['y']=od_y
                    sub['angle']=angle
        return sub

    def plastic2(self, img, threshold = (176, 255), close = 3, ratio = 0.73, min_area = 5000, max_area = 50000):
        img.binary([threshold])
        if close != 0:
            img.close(close)
        sub = {}
        for b in img.find_blobs([threshold], pixels_threshold = 100, area_threshold = 4000):
            if b.area() > min_area and b.area() < max_area:
		    l = b.major_axis_line()
		    angle = self.math.atan2(l[1] - l[3], l[0] - l[2])

		    if self.distance(b.cx(), b.cy(), l[0], l[1]) > self.distance(b.cx(), b.cy(), l[2], l[3]):
			angle = angle + self.math.radians(180)
		    angle = angle + self.math.radians(180)
		    angle = angle - self.math.radians(6)
		    c2x = int(b.cx() + 95 * self.math.cos(angle))
		    c2y = int(b.cy() + 95 * self.math.sin(angle))
		    img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(0, 255, 0), thickness = 3)
		    img.draw_cross(b.cx(), b.cy(), color=(0, 255, 0), thickness = 3)

		    angle = self.math.degrees(angle)
		    if angle < 0:
			angle = angle + 360
		    if angle > 360:
			angle = angle - 360
		    angle = angle - 180

		    #        w    h
		    shape = 800, 600
		    center = shape[0]/2, shape[1]/2
		    # Oś X
		    od_x = (b.cx() - center[0]) * ratio
		    # Oś Y
		    od_y = (b.cy() - center[1]) * ratio

		    sub['x'] = od_x
		    sub['y'] = od_y
		    sub['angle']=angle
        return sub
