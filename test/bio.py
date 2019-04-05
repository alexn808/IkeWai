from __future__ import print_function
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
                text = raw_input("If you want to keep recording data press 1 else press 0")
                if text == "0":
                        break

totData = json.dumps(data1)
rgbData = json.dumps(dataRGB)
avgGreen = totGreen/count
avgRed = totRed/count
avgBlue = totBlue/count

timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
print("Uploading Data...")
name4data = ("total_data" + timestamp)
f = open(name4data.json, "w")
f.write(totData)
f.close()
print(data1)
print("Average Green %.2f" % avgGreen)
print("Average Red %.2f" % avgRed)
print("Average Blue %.2f" % avgBlue)

