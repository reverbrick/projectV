import sensor, image, time, os, tf, math
snapshot_source = False

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

#threshold = (39, 70, 30, 77, 21, 65)
threshold = (94, 255)
ratio = 1.2
c_point = (320,240)
stream = None
if snapshot_source == False:
    stream = image.ImageIO("velux/velux-plastik2/grayscale/auto.bin", "r")

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

while(True):
    if snapshot_source:

        img = sensor.snapshot()

    else:

        img = stream.read(copy_to_fb=True, loop=True, pause=True)
        #img.binary([threshold])

        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):

            major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) + ((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
            minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) + ((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))

            # Uncoment if something went wrong
            #img.draw_string(b.cx(), b.cy(), "%s"%b.pixels())
            #img.draw_string(b.cx(), b.cy(), "%s"%(major_len/minor_len))
            if major_len/minor_len > 4 and major_len/minor_len < 6:

                if b.pixels() > 2700 and b.pixels() < 2900:

                    l = b.major_axis_line()
                    angle = math.atan2(l[1] - l[3], l[0] - l[2])

                    if distance(b.cx(), b.cy(), l[0], l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):

                        angle = angle + math.radians(180)
                        angle = angle + math.radians(5)
                        c1x = int(b.cx() + 92 * math.cos(angle))
                        c1y = int(b.cy() + 92 * math.sin(angle))

                    else:

                        angle = angle - math.radians(5)
                        c1x = int(b.cx() + 92 * math.cos(angle))
                        c1y = int(b.cy() + 92 * math.sin(angle))
                    angle = math.degrees(angle)

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
                            img.draw_rectangle(rect[0], rect[1] - 10,rect[2], 10, (255, 255, 255), fill=True)
                            img.draw_string(rect[0], rect[1]-10, "Pick position", (0, 0, 0))
                            img.draw_string(rect[0], rect[1], "x: %s"%round((b.cx() - c_point[0]) * ratio, 5) + " mm")
                            img.draw_string(rect[0], rect[1]+10, "y: %s"%round((b.cy() - c_point[1]) * ratio, 5) + " mm")
                            img.draw_string(rect[0], rect[1]+20, "angle: %s"%angle+"°")
                            img.draw_cross(b.cx(), b.cy(),(255, 255, 255), 6, 3)
                            img.draw_arrow(b.cx(), b.cy(), c1x, c1y, (255, 255, 255), 4)
                    except:
                        pass
