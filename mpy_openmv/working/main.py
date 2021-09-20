from machine import UART
from ioia import Camera, Flash, Velux; import time
from comms import recv_msg, send_msg
import math, json
cam = Camera(exposure=44000, framesize="SVGA")
cam.sensor.set_quality(100)
cam.sensor.set_contrast(-3)
cam.sensor.set_brightness(-3)
fla = Flash(0.1,0)
ser = UART(3, 115200)
ratio = 0.73
def distance(x1,y1,x2,y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
while(True):
	buf = recv_msg(ser)
	if buf==b"snap":
		img = cam.snap(fla, corr=0.9)
		h = img.get_histogram()
		t = h.get_threshold()[0]
		out = []
		for b in img.find_blobs([(t,255)], merge=False, pixels_threshold=3800):
			ret = {}
			pix = b.pixels()
			if pix<6500:
				c = b.corners()
				l = b.major_axis_line()
				angle = math.atan2(l[1] - l[3], l[0] - l[2])
				if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(),l[2],l[3]):
					angle = angle + math.radians(180)
					mmratio = distance(b.cx(), b.cy(),l[0],l[1]) / distance(b.cx(), b.cy(),l[2],l[3])
				else:
					mmratio = distance(b.cx(), b.cy(),l[2],l[3]) / distance(b.cx(), b.cy(),l[0],l[1])
				img.draw_edges(c)
				if mmratio>1.3 and mmratio<1.7:
					c2x = int(b.cx() + 80 * math.cos(angle))
					c2y = int(b.cy() + 80 * math.sin(angle))
					img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,0,0))
					img.draw_cross(b.cx(), b.cy(), color=(255,0,0))
					img.draw_line(b.major_axis_line(), color=(255,0,0))
					img.draw_line(b.minor_axis_line(), color=(255,0,0))
					c_point = (320,240)
					ret['x']=round((b.cx()-c_point[0])*ratio,5)
					ret['y']=round((b.cy()-c_point[1])*ratio,5)
					ret['pix'] = pix
					angle = math.degrees(angle)
					if angle>180:
						angle=angle-360
					ret['angle']=round(angle,5)
					out.append(ret)
		send_msg(ser,bytearray(json.dumps(out)))
	time.sleep(0.5)