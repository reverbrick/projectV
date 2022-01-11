import sensor, image, time, math
from pyb import Pin
delay = 0.3
threshold = (124, 255)
def distance(x1,y1,x2,y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
def blobs(img, threshold):
	ret = {}
	for b in img.find_blobs([(127,255)], pixels_threshold=700, area_threshold=5000, merge=False):
		if b.pixels()<8000:
			print(b.density())
			l = b.major_axis_line()
			angle = math.atan2(l[1] - l[3], l[0] - l[2])
			if distance(b.cx(), b.cy(),l[0],l[1]) > distance(b.cx(), b.cy(),l[2],l[3]):
				angle = angle - math.radians(180)
			c2x = int(b.cx() + 80 * math.cos(angle))
			c2y = int(b.cy() + 80 * math.sin(angle))
			img.draw_arrow(b.cx(), b.cy(), c2x, c2y, color=(255,0,0))
			img.draw_cross(b[5], b[6], color=(255,0,0))
			img.draw_line(b.major_axis_line(), color=(255,0,0))
			img.draw_line(b.minor_axis_line(), color=(255,0,0))
			ret['x']=b.cx()
			ret['y']=b.cy()
			ret['angle']=math.degrees(angle)
	return ret
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.set_auto_exposure(True)
sensor.set_auto_gain(True)
sensor.set_auto_whitebal(True)
sensor.set_contrast(0)
sensor.set_brightness(0)
sensor.skip_frames(20)
def get(threshold=threshold):
	start = time.ticks_ms()
	pin0.value(1)
	img = sensor.snapshot()
	pin0.value(0)
	img.binary([threshold])
	img.close(5)
	ret = blobs(img, threshold)
	print(ret)
#	time.sleep(delay)