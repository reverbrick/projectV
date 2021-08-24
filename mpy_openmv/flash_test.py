# Untitled - By: reverbrick - wt. sie 24 2021

import time
from pyb import Pin
pin = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
while True:
    pin.value(1)
    time.sleep_ms(10)
    pin.value(0)
    time.sleep(0.2)
