#works only on NUCLEO_F767ZI

#building cross compiler
make -C mpy-cross

cd ports/stm32
make submodules
make

#flashing using stlink
make -C ports/stm32 MICROPY_HW_ENABLE_ETH_RMII=1 BOARD=NUCLEO_F767ZI deploy-stlink

#accessing via screen
screen /dev/ttyACM0 115200

#repl comment here:
lib/utils/pyexec.c
mp_hal_stdout_tx_str("Proudly brought to you by IOIA/ReverbLand. For support please email Daniel Gorny at dadmin.dgor@gmail.com\r\n");

#recover if bad things happen
st-flash erase
#and reflash
