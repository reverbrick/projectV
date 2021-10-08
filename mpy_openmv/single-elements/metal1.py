import sensor, image, time, os, tf, math

snapshot_source = False

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

stream = None
threshold = (4, 100, -6, 65, -39, 49)
ratio = 1.2
c_point = (400,300)

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
if snapshot_source == False:
    stream = image.ImageIO("/velux/velux-metal/rgb/manual.bin", "r")

while(True):
    if snapshot_source:
        img = sensor.snapshot()
    else:
        img = stream.read(copy_to_fb=True, loop=True, pause=True)
        #img.binary([threshold])
        for b in img.find_blobs([threshold], pixels_threshold = 2000, area_threshold = 4000):

            if b.pixels() > 3200 and b.pixels() < 5000:
                rect = b.rect()
                l = b.major_axis_line()
                roi = (b.cx()-5, b.cy()-5, 10, 10)
                major_len = math.sqrt(((b.major_axis_line()[0] - b.major_axis_line()[2])**2) +((b.major_axis_line()[1] - b.major_axis_line()[3])**2))
                minor_len = math.sqrt(((b.minor_axis_line()[0] - b.minor_axis_line()[2])**2) +((b.minor_axis_line()[1] - b.minor_axis_line()[3])**2))
                stats = img.get_statistics(roi=roi)

                # Uncoment if something went wrong for get each parameter
                #img.draw_string(b.cx()-5, b.cy()-15, "%s"%stats[0]+ " %s"%stats[1], scale = 1)
                #img.draw_string(b.cx(), b.cy(), "%s"%(major_len/minor_len))
                #img.draw_string(b.cx(), b.cy(), "%s"%b.pixels())
                #img.draw_recangle(roi)

                if stats[0] >= 28:

                    if major_len/minor_len > 9 and major_len/minor_len < 12:

                        angle = math.atan2(l[1] - l[3], l[0] - l[2])
                        if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                            angle = angle + math.radians(180)

                        c2x = int(b.cx() - 100 * math.cos(angle))
                        c2y = int(b.cy() - 100 * math.sin(angle))
                        angle = math.degrees(angle)
                        if angle < 0:
                            angle=angle+180

                        if angle > 180:
                            angle=angle-180

                        img.draw_arrow(b.cx(), b.cy(), c2x, c2y, (255,255,255), 4)
                        img.draw_cross(b.cx(), b.cy(), (0,255,0), size = 10, thickness = 3)
                        img.draw_rectangle(b.rect(), color= (0,255,0))
                        img.draw_rectangle(rect[0],rect[1]-10,rect[2], 10, (0,255,0), fill=True)
                        img.draw_string(rect[0],rect[1]-10, "Top position", (0,0,0))
                        img.draw_string(rect[0],rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio,5)+" mm")
                        img.draw_string(rect[0],rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio,5)+" mm")
                        img.draw_string(rect[0],rect[1]+20, "angle: %s"%angle+"°")


                else:
                    angle = math.atan2(l[1] - l[3], l[0] - l[2])
                    if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(), l[2], l[3]):
                        angle = angle + math.radians(180)

                    angle = angle + math.radians(270)
                    c2x = int(b.cx() - 10 * math.cos(angle))
                    c2y = int(b.cy() - 10 * math.sin(angle))

                    angle = angle - math.radians(90)
                    c3x = int(c2x + 115 * math.cos(angle))
                    c3y = int(c2y + 115 * math.sin(angle))

                    angle = math.degrees(angle)
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

                            img.draw_cross(b.cx(), b.cy(), (0,0,255), size = 10, thickness = 3)
                            img.draw_arrow(c2x, c2y, c3x, c3y)
                            img.draw_rectangle(b.rect(), color= (0,0,255))
                            img.draw_rectangle(rect[0],rect[1]-10,rect[2], 10, (0,0,255), fill=True)
                            img.draw_string(rect[0],rect[1]-10, "Right position", (0,0,0))
                            img.draw_string(rect[0],rect[1], "x: %s"%round((b.cx()-c_point[0])*ratio,5)+" mm")
                            img.draw_string(rect[0],rect[1]+10, "y: %s"%round((b.cy()-c_point[1])*ratio,5)+" mm")
                            img.draw_string(rect[0],rect[1]+20, "angle: %s"%angle+"°")

                    except:
                        pass
