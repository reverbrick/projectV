import sensor, image, time, os, tf
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
net = "trained.tflite"
labels = [line.rstrip('\n') for line in open("labels.txt")]
clock = time.clock()
while(True):
	clock.tick()
	img = sensor.snapshot()
	for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
		print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
		img.draw_rectangle(obj.rect())
		predictions_list = list(zip(labels, obj.output()))
		for i in range(len(predictions_list)):
			print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))
	print(clock.fps(), "fps")