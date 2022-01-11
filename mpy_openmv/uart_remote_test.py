from machine import UART
import time
from pyb import LED
ser = UART(3, 115200)
led = LED(1)
while True:
    if ser.any():
    #if True:
        buf = ser.readline()
        led.on()
        ser.write('{"foo":"bar"}')
        time.sleep(0.1)
        led.off()
    time.sleep(0.3)
