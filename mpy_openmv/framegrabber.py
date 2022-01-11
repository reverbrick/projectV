import image, network, omv, rpc, sensor, struct

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

omv.disable_fb(True)

#interface = rpc.rpc_usb_vcp_slave()
#interface = rpc.rpc_uart_slave(baudrate=7500000)
interface = rpc.rpc_uart_slave(baudrate=115200)

def jpeg_image_snapshot(data):
    pixformat, framesize = bytes(data).decode().split(",")
    sensor.set_pixformat(eval(pixformat))
    sensor.set_framesize(eval(framesize))
    exposure=0 #todo
    if exposure == 0:
        sensor.set_auto_exposure(True)
    else:
        sensor.set_auto_exposure(False, exposure_us=exposure)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False)

    img = sensor.snapshot().compress(quality=80)
    return struct.pack("<I", img.size())

def raw_image_snapshot(data):
    pixformat, framesize = bytes(data).decode().split(",")
    sensor.set_pixformat(eval(pixformat))
    sensor.set_framesize(eval(framesize))
    exposure=0 #todo
    if exposure == 0:
        sensor.set_auto_exposure(True)
    else:
        sensor.set_auto_exposure(False, exposure_us=exposure)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False)

    img = sensor.snapshot()
    return struct.pack("<I", img.size())

def image_read_cb():
    interface.put_bytes(sensor.get_fb().bytearray(), 5000) # timeout

def image_read(data):
    if not len(data):
        interface.schedule_callback(image_read_cb)
        return bytes()
    else:
        offset, size = struct.unpack("<II", data)
        return memoryview(sensor.get_fb().bytearray())[offset:offset+size]

# Register call backs.

interface.register_callback(raw_image_snapshot)
interface.register_callback(jpeg_image_snapshot)
interface.register_callback(image_read)

interface.loop()
