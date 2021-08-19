#!/bin/bash
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/utelnet/utelnetserver.py -o utelnet.mpy
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/urequests/urequests/__init__.py -o urequests.mpy
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/robot.py -o robot.mpy
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/camera.py -o camera.mpy
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/stepper.py -o stepper.mpy
~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_nucleo/comms.py -o comms.mpy

~/Documents/Stuff/micropython/mpy-cross/mpy-cross ../mpy_openmv/ioia.py -o ioia.mpy
