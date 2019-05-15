# importing all the libraries we are using
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
import socket
import logging
from pymongo import MongoClient
# Since this library is in another folder we need to insert a path to be able to access the library
sys.path.insert(0, '/home/pi/Desktop/ikewai/lib')
import iw_rgb

# I2C stuff
bus = smbus.SMBus(1)
totGreen = 0
totBlue = 0
totRed = 0
count = 0
data1 = []
dataRGB = {}

# This is to return what parts per X in solution you are testing

def parts_per(value):
    ppX = {
	   1: "ppt",
           2: "pph",
           3: "ppth",
           4: "pptth",
           5: "pphth",
           6: "ppm",
           7: "pptm",
           8: "pphm",
           }
    x = int(value)
    # If the value is within the range of what we are testing then
    # we return the value, if not we return an Error
    if x > 0 & x < 9:
        return ppX.get(x, "Within Range")
    else:
        return "Error"
# Used to display how diluted the solution you are testing
ppX = {
    1: "parts per ten (ppt, 1:10)",
    2: "parts per hundred (pph 1:100)",
    3: "parts Per thousand (ppth 1:1000)",
    4: "parts per ten thousand (pptth 1:10000)",
    5: "parts per hundred thousand (pphth 1:100000)",
    6: "parts per million (ppm 1:1000000)",
    7: "parts per ten million (ppm 1:10000000)",
    8: "parts per hundred million (pphm 1:100000000)",
}

if __name__ == "__main__":

    # Asking for user input
    nameoffile = raw_input("What is liquid you are testing? ")
    # Printing ppx for user input
    print(json.dumps(ppX, indent=4, sort_keys=True))
    parts = raw_input("Select how diluted your solution is: ")
    parts = parts_per(parts)
    while True:
        # Sleeps for 1 second
        time.sleep(0.2)
        # Turn on LED
        iw_rgb.turn_led_on()

        # Reading and converting the data from the sensor to something readable
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
        # Store the Data into a dictionary
        dataRGB = {'Green': green,
                   'Red': red,
                   'Blue': blue}
        # Writing data into dictionary and appending them
        data1.append(dataRGB)
        # Adding up the total amount of RGB values to compute averages later
        totGreen += green
        totRed += red
        totBlue += blue
        count += 1

        # print RGB values to see current values
        print("green: %.2f" % green)
        print("red: %.2f" % red)
        print("blue: %.2f" % blue)
        # Sleep for 0.5 seconds so it is more readable
        time.sleep(0.1)
	print"-----------"
        # Turn off LED
        iw_rgb.turn_led_off()
        # Records 3 samples then asks you if you want to record again
        if count % 100 == 0:
            text = raw_input("To stop recording data enter 0")
            if text == "0":
                break
    # Computing the averages of all the data
    avgGreen = totGreen/count
    avgRed = totRed/count
    avgBlue = totBlue/count
    data1.append({'Average Green': avgGreen,
                  'Average Red': avgRed,
                  'Average Blue': avgBlue})
    # Converting data into a json format
    totData_json = json.dumps(data1)
    rgbData_json = json.dumps(dataRGB)


    # Writing save location and names
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    save_path = '/home/pi/Desktop/ikewai/Flourescence'
    name4data = nameoffile + " " + parts + " " + timestamp
    completeName = os.path.join(save_path, '%s.json' % name4data)

    # Creating the files
    print("Saving Data...")
    f = open(completeName, "w+")
    f.write(totData_json)
    f.close()

    # Setting up the client to start upload
    client = pymongo.MongoClient("mongodb+srv://Ryan:Fablab1@biofinder-rgsud.gcp.mongodb.net/admin")
    db = client['BioFinder1']
    totData_db = db[nameoffile + parts]

    print("Uploading Data...")

    # Opens up the file we are trying to upload and uploads it to the server client
    with open('%s.json' % name4data) as f:
        file_data = json.load(f)
        totData_db.insert(file_data)

    print("Done")

    # Close client
    client.close()

    # Printing the averages for the RGB values
    print(data1)
    print("Average Green %.2f" % avgGreen)
    print("Average Red %.2f" % avgRed)
    print("Average Blue %.2f" % avgBlue)

    # Future Improvements:
    # with data collected, you have averages and can implement
    # a function to detect what liquid you are in


