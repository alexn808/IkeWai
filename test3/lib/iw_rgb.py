from __future__ import division
import time
import RPi.GPIO as GPIO
import smbus
import math


led_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_pin, GPIO.OUT)


def turn_led_on():
    GPIO.output(led_pin, GPIO.HIGH)


def turn_led_off():
    GPIO.output(led_pin, GPIO.LOW)


# I2C stuff
bus = smbus.SMBus(1)


def get_rgb():
    for i in range(0,1):

        bus.write_byte_data(0x44, 0x01, 0x0D)
        data = bus.read_i2c_block_data(0x44, 0x09, 6)

        # convert data
        green = data[1] * 256 + data[0]
        red   = data[3] * 256 + data[2]
        blue  = data[5] * 256 + data[4]

        # light source exceeds 255 lux value of the sensor
        # we want to keep the RGB value within 8 bits
        # LSR by however many bits exceed the 8 bit limit
        # i.e. if the input is 10 bits, the value will be shifted right$
        if (green > 255 or red > 255 or blue > 255):
                # determine maximum color value
                max_color = max(green, red, blue)
                # determine how many bits exceeded the 8 bit limit
                exceed_bits = math.ceil(math.log(max_color,2) - 8)
                # update value (LSR exceed_bits)
                green = int(green / math.pow(2,exceed_bits))
                red   = int(red   / math.pow(2,exceed_bits))
                blue  = int(blue  / math.pow(2,exceed_bits))

        #Pprint RGB values.
        # print "green: %.2f" %green
        # print "red: %.2f" %red
        # print "blue: %.2f" %blue

        return [red,green,blue]

        time.sleep(1)
