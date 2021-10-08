import sensor, image, time, os, tf, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

threshold = (28, 86, 9, 86, -2, 64)
ratio = 1.2
c_point = (400,300)
snapshot_source = False
stream = None

if snapshot_source == False:
    stream = image.ImageIO("/velux/velux-plastik/grayscale/auto.bin", "r")

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

while(True):
    if snapshot_source:
        img = sensor.snapshot()
    else:
        img = stream.read(copy_to_fb=True, loop=True, pause=True)
        out = []
        for b in img.find_blobs([threshold], merge=False, pixels_threshold=3800):
            ret = {}
            pix = b.pixels()
            if pix > 3000 and pix < 7000:
                c = b.corners()
                l = b.major_axis_line()
                angle = math.atan2(l[1] - l[3], l[0] - l[2])
                if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(),l[2],l[3]):
                    angle = angle + math.radians(180)
                    mmratio = distance(b.cx(), b.cy(),l[0],l[1]) / distance(b.cx(), b.cy(),l[2],l[3])
                else:
                    mmratio = distance(b.cx(), b.cy(),l[2],l[3]) / distance(b.cx(), b.cy(),l[0],l[1])
                if mmratio>1.3 and mmratio<1.7:
                    angle = angle + math.radians(180)
                    c2x = int(b.cx() + 80 * math.cos(angle))
                    c2y = int(b.cy() + 80 * math.sin(angle))

                    major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                    minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                    if major_len / minor_len > 1.72 and major_len / minor_len < 2.1:
                        rect = b.rect()
                        img.draw_rectangle(rect[0],rect[1]-10,rect[2], 10, (255,255,255), fill=True)
                        img.draw_rectangle(rect)
                        img.draw_string(rect[0],rect[1]-10, "Pick position", (0,0,0))
                        img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,255,255), thickness = 3)
                        img.draw_cross(b.cx(), b.cy(), color=(255,255,255), size = 5, thickness = 3)
                        #img.draw_edges(c)
                        angle = math.degrees(angle)
                        if angle<0:
                            angle=angle+360
                        if angle>180:
                            angle=angle-360
                        ret['x']=round((b.cx()-c_point[0])*ratio,5)
                        ret['y']=round((b.cy()-c_point[1])*ratio,5)
                        ret['pix'] = pix
                        ret['angle']=round(angle,5)
                        img.draw_string(rect[0],rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio,5)+" mm")
                        img.draw_string(rect[0],rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio,5)+" mm")
                        img.draw_string(rect[0],rect[1]+20, "angle: %s"%angle+"°")
