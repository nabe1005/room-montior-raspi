#!/usr/bin/env python3

import serial
import time
import datetime
import json
import argparse
import sys


class MHZ14A():
    PACKET = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    ZERO = [0xff, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]

    def __init__(self, ser):
        self.serial = serial.Serial(ser, 9600, timeout=1)
        time.sleep(2)

    def zero(self):
        self.serial.write(bytearray(MHZ14A.ZERO))

    def get(self):
        self.serial.write(bytearray(MHZ14A.PACKET))
        res = self.serial.read(size=9)
        res = bytearray(res)
        checksum = 0xff & (~(res[1] + res[2] + res[3] + res[4] + res[5] + res[6] + res[7]) + 1)
        if res[8] == checksum:
            return ((res[2] << 8) | res[3])
        else:
            raise Exception("checksum: " + hex(checksum))

    def close(self):
        self.serial.close()


def get_co2():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    args = parser.parse_args()
    mode = args.mode or "co2"

    co2 = MHZ14A("/dev/ttyAMA0")

    if mode == "zero":
        co2.zero()
    else:
        try:
            data = co2.get()
            co2.close()
            return data
        except:
            # 本当はエラーハンドリングをする
            co2.close()
            return int(-1)

def main():
    print(get_co2())

if __name__ == "__main__":
    main()