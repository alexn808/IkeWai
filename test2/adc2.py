from __future__ import division
import smbus
import time


def convert_to_digital(data_array):
    raw_adc = data_array[0] * 256 + data_array[1]

    if raw_adc > 32767:
        raw_adc -= 65535

    digital_voltage = raw_adc / 32767 * 6.144

    return digital_voltage


# Get I2C bus
bus = smbus.SMBus(1)

# ADS1115 address, 0x48
# Select configuration register, 0x01
# 0xC083 and 0xD083(1000000010000011 binary) AINP = AIN0 and AINN = AIN1, +/- 6.144 V
# Continuous conversion mode, 128SPS

# ADS1115 address, 0x48
# Read data back from 0x00, 2 bytes in array (raw_adc MSB, raw_adc LSB)

data0 = [0xC0, 0x83]
data1 = [0xD0, 0x83]

while True:

    bus.write_i2c_block_data(0x48, 0x01, data0)
    time.sleep(0.5)
    data00 = bus.read_i2c_block_data(0x48, 0x00, 2)
    time.sleep(0.5)

    bus.write_i2c_block_data(0x48, 0x01, data1)
    time.sleep(0.5)
    data11 = bus.read_i2c_block_data(0x48, 0x00, 2)
    time.sleep(0.5)

    print("A0 to GND (V): " + str(convert_to_digital(data00)))
    print("A1 to GND (V): " + str(convert_to_digital(data11)))
    time.sleep(1)
