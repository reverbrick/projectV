ratio=0.73
#ratio=1.35

class Camera():
    import sensor
    def __init__(self, color=False, exposure=None, small=False, contrast=0, brightness=0):
        self.sensor.reset()
        if color:
            self.sensor.set_pixformat(self.sensor.RGB565)
        else:
            self.sensor.set_pixformat(self.sensor.GRAYSCALE)
        if small:
            self.sensor.set_framesize(self.sensor.QVGA)
        else:
            self.sensor.set_framesize(self.sensor.VGA)
        if exposure == None:
            self.sensor.set_auto_exposure(True)
        else:
            self.sensor.set_auto_exposure(False, exposure_us=exposure)
        self.sensor.set_contrast(contrast)
        self.sensor.set_brightness(brightness)
        self.sensor.skip_frames(time = 2000)
        self.sensor.set_auto_gain(False)
        self.sensor.set_auto_whitebal(False)

    def snap(self, flash = None):
        if flash:
            flash.on()
        img = self.sensor.snapshot()
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
        self.time.sleep(self.pre)

    def off(self):
        self.time.sleep(self.post)
        self.pin.value(0)


class Velux():
    import math
    def distance(self,x1,y1,x2,y2):
        return self.math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def plastic(self, img, threshold=(103, 255), close=3, min=2300, max=4000, debug=False, ratio=0.73):
        ret = {}
        #img.mask_circle([130,470,450])
        #img.draw_circle([120,480,80], color=(0,0,0),fill=True)
        img.binary([threshold])
        img.close(close)
        for b in img.find_blobs([(255,255)], pixels_threshold=min, merge=False):
            if b.pixels()<max:
                #print(b.pixels())
                #blob rotation
                l = b.major_axis_line()
                #angle from 2 points
                angle = self.math.atan2(l[1] - l[3], l[0] - l[2])
                #angle correction based on distance
                if self.distance(b.cx(), b.cy(),l[0],l[1]) > self.distance(b.cx(), b.cy(),l[2],l[3]):
                    angle = angle + self.math.radians(180)
                c2x = int(b.cx() + 80 * self.math.cos(angle))
                c2y = int(b.cy() + 80 * self.math.sin(angle))
                img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,0,0))
                img.draw_cross(b.cx(), b.cy(), color=(255,0,0))
                img.draw_line(b.major_axis_line(), color=(255,0,0))
                img.draw_line(b.minor_axis_line(), color=(255,0,0))
                c_point = (320,240)
                ret['x']=round((b.cx()-c_point[0])*ratio,5)
                ret['y']=round((b.cy()-c_point[1])*ratio,5)
                angle = self.math.degrees(angle)
                #if angle<0:
                #    angle=angle+360
                if angle>180:
                    angle=angle-360
                ret['angle']=angle
        if debug:
            img.save("debug.jpg")
        return ret

    def metal(self, img, threshold, single=False):
        ret = {'items':[]}
        for b in img.find_blobs([threshold], pixels_threshold=3000, area_threshold=100, merge=False):
            sub = {}
            #print(b)
            for s in img.find_blobs([threshold], roi=(b[0:4]), invert=True, merge=False):
                #print(s)
                if s[4]>150 and s[4]<320:
                    img.draw_rectangle(s[0:4], color=(0,0,0))
            #draw arrow
            c2x = int(b.cx() + 30 * self.math.cos(b.rotation()))
            c2y = int(b.cy() + 30 * self.math.sin(b.rotation()))
            img.draw_arrow(b.cx(), b.cy(), c2x, c2y)
            img.draw_rectangle(b[0:4], color=(0,0,0))
            img.draw_cross(b[5], b[6], color=(0,0,0))
            sub['x']=b.cx()
            sub['y']=b.cy()
            sub['angle']=self.math.degrees(b.rotation())
            sub['pixels']=b.pixels()
            sub['density']=b.density()
            ret['items'].append(sub)
            if single:
                break
        return ret
