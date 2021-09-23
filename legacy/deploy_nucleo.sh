#!/bin/bash
#cd ~/Documents/Stuff/micropython/
#make -C ports/stm32 MICROPY_HW_ENABLE_ETH_RMII=1 BOARD=NUCLEO_F767ZI deploy-stlink
cd /mnt/NewOrder/velux/mpy_nucleo/
#mpremote a0 fs cp mpy_libs/*.mpy :
mpremote a0 fs cp utelnet/utelnetserver.py :utelnet.py
mpremote a0 fs cp urequests/urequests/__init__.py :urequests.py
mpremote a0 fs cp camera.py :
#mpremote a0 fs cp common.py :
mpremote a0 fs cp comms.py :
mpremote a0 fs cp robot.py :
mpremote a0 fs cp stepper.py :
mpremote a0 fs cp main_simple.py :main.py
mpremote a0 fs cp boot.py :
