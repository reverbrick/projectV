import sensor, image, time, os, tf, math
snapshot_source = False

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

threshold = (14, 255)
ratio = 1.2
c_point = (400,300)

stream = None
if snapshot_source == False:
    stream = image.ImageIO("velux/velux-metal2/grayscale/auto.bin", "r")

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

while(True):
    if snapshot_source:
        img = sensor.snapshot()
    else:
        img = stream.read(copy_to_fb=True, loop=True, pause=True)
        #img.binary([threshold])
        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):
            if b.pixels() > 3000 and b.pixels() < 5900:
                major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                if major_len/minor_len > 7 and major_len/minor_len < 9:
                    l = b.major_axis_line()
                    angle = math.atan2(l[1] - l[3], l[0] - l[2])
                    if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + math.radians(180)

                    angle = angle + math.radians(180)
                    c1x = int(b.cx() + 100 * math.cos(angle))
                    c1y = int(b.cy() + 100 * math.sin(angle))

                    angle = angle - math.radians(270)
                    c2x = int(b.cx() - 8 * math.cos(angle))
                    c2y = int(b.cy() - 8 * math.sin(angle))

                    angle = angle + math.radians(270)
                    c3x = int(c2x + 112 * math.cos(angle))
                    c3y = int(c2y + 112 * math.sin(angle))
                    roi = (c3x-2, c3y-2, 4, 4)

                    try:
                        stats = img.get_statistics(roi=roi, thresholds=[threshold])
                        rect = b.rect()
                        if stats[0] == 0:
                            img.draw_rectangle(b.rect(), color= (0,255,0))
                            angle = math.degrees(angle)

                            if angle > 180:
                                angle = angle - 360

                            # Uncoment if something went wrong
                            #img.draw_string(b.cx(), b.cy(), "%s"%angle)
                            #img.draw_rectangle(roi)

                            img.draw_rectangle(rect[0],rect[1]-10,rect[2], 10, (0,255,0), fill=True)
                            img.draw_rectangle(b.rect(), color=(0,255,0))
                            img.draw_string(rect[0],rect[1]-10, "Pick position", (255,255,255))
                            img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx() - c_point[0]) * ratio, 5) + " mm")
                            img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy() - c_point[1]) * ratio, 5) + " mm")
                            img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")
                            img.draw_cross(b.cx(), b.cy(), (255,255,255), 8, 2)
                            img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (255,255,255), 2)
                    except:
                        pass
