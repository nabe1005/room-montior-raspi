#coding: utf-8

from smbus import SMBus
from common import *
import time


def readData():
    data = []
    global temp_result
    for i in range(0xF7, 0xF7+8):
        data.append(bus.read_byte_data(i2c_address, i))
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    temp_result = compensate_T(temp_raw)


def temp_start():
    setup()
    get_calib_param()
    readData()
    return temp_result


if __name__ == '__main__':
    try:
        readData()
    except KeyboardInterrupt:
        pass
