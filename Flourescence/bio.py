from __future__ import division
import smbus
import RPi.GPIO as GPIO
import datetime
import time
import math
import json
import sys
import os
import pymongo
from pymongo import MongoClient
import lib.iw_rgb

# I2C stuff
bus = smbus.SMBus(1)
totGreen = 0
totBlue = 0
totRed = 0
count = 0
data1 = []
dataRGB = {}


def parts_per(value):
    ppX = {1: "pph",
           2: "ppt",
           3: "pptt",
           4: "ppht",
           5: "ppm",
           6: "pptm",
           7: "pphm",
           8: "ppb",
    }
    return ppX.get(value, "error! try again")


ppX = {
    1: "parts per hundred (pph, 1:100)",
    2: "parts per thousand (ppt 1:1000)",
    3: "parts Per ten thousand (pptt 1:10000)",
    4: "parts per hundred thousand (ppht 1:100000)",
    5: "parts per million (ppm 1:1000000)",
    6: "parts per ten million (pptm 1:10000000)",
    7: "parts per hundred million (pphm 1:100000000)",
    8: "parts per billion (ppb 1:1000000000)",
       }
if __name__ == "__main__":

    nameoffile = raw_input("What is liquid you are testing?")
    print(json.dumps(ppX, indent=4, sort_keys=True))
    parts = raw_input("Select how diluted your solution is:")
    while True:
        #turn UV LED on? No it sleeps waits 1 second
        time.sleep(1)
        lib.iw_rgb.turn_led_on()
        bus.write_byte_data(0x44, 0x01, 0x0D)
        data = bus.read_i2c_block_data(0x44, 0x09, 6)

        # convert data
        green = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        blue = data[5] * 256 + data[4]

        # light source exceeds 255 lux value of the sensor
        # we want to keep the RGB value within 8 bits
        # LSR by however many bits exceed the 8 bit limit
        # i.e. if the input is 10 bits, the value will be shifted right$
        if green > 255 or red > 255 or blue > 255:
            # determine maximum color value
                max_color = max(green, red, blue)
                # determine how many bits exceeded the 8 bit limit
                exceed_bits = math.ceil(math.log(max_color, 2) - 8)
                # update value (LSR exceed_bits)
                green = int(green / math.pow(2, exceed_bits))
                red   = int(red   / math.pow(2, exceed_bits))
                blue  = int(blue  / math.pow(2, exceed_bits))

        dataRGB = {'Green': green,
                'Red': red,
                'Blue': blue}

        data1.append(dataRGB)
        totGreen += green
        totRed += red
        totBlue += blue
        count += 1
        # print RGB values - comment out later
        print("green: %.2f" % green)
        print("red: %.2f" % red)
        print("blue: %.2f" % blue)
        time.sleep(0.5)
        lib.iw_rgb.turn_led_off()
        if count % 3 == 0:
            text = raw_input("To stop recording data enter 0")
            if text == "0":
                break

    totData_json = json.dumps(data1)
    rgbData_json = json.dumps(dataRGB)
    print(totData_json)
    avgGreen = totGreen/count
    avgRed = totRed/count
    avgBlue = totBlue/count

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    print("Uploading Data...")
    name4data = (nameoffile + " " +  parts + " " + timestamp)
    f = open(name4data.json, "w")
    f.write(totData)
    f.close()
    print(data1)
    print("Average Green %.2f" % avgGreen)
    print("Average Red %.2f" % avgRed)
    print("Average Blue %.2f" % avgBlue)

