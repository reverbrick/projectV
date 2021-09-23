#Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Górny at dadmin.dgor@gmail.com
import pyb, time

def heartbeat():
    while True:
        pyb.LED(1).on()
        time.sleep(0.01)
        pyb.LED(1).off()
        time.sleep(0.01)
        yield None

def run():
    while True:
        pyb.LED(2).on()
        time.sleep(0.01)
        pyb.LED(2).off()
        time.sleep(0.01)
        yield None

def error():
    while True:
        pyb.LED(3).on()
        time.sleep(0.01)
        pyb.LED(3).off()
        time.sleep(0.01)
        yield None
