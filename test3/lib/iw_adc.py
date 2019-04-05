# Author:   Alex Noveloso
# Date:     November 13, 2018
# Notes:    Max voltage to analog inputs should be VDD +0.3V
#           VDD min = -0.3 V
#           VDD min = 7.0 V
#           Plan to set VDD to 5 V, so max analog inputs should be 5.3V

from __future__ import division
import smbus
import time


def get_adc0():

    # Get I2C bus
    bus = smbus.SMBus(1)

    # ADS1115 address, 0x48
    # Select configuration register, 0x01
    # 0x8083(1000000010000011 binary) AINP = AIN0 and AINN = AIN1, +/- 6.144 V
    # Continuous conversion mode, 128SPS

    data = [0xC0, 0x83]
    bus.write_i2c_block_data(0x48, 0x01, data)
    time.sleep(1)

    # ADS1115 address, 0x48(72)
    # Read data back from 0x00(00), 2 bytes
    # raw_adc MSB, raw_adc LSB
    data = bus.read_i2c_block_data(0x48, 0x00, 2)

    # print(data)
    # Convert the data
    raw_adc = data[0] * 256 + data[1]

    # if raw_adc > 32767:
    # 	raw_adc -= 65535

    digital_voltage = raw_adc / 32767 * 6.144

    #print("Digital Voltage (V): " + str(digital_voltage))

    return digital_voltage


def get_adc1():

    # Get I2C bus
    bus = smbus.SMBus(1)

    # ADS1115 address, 0x48
    # Select configuration register, 0x01
    # 0x8083(1000000010000011 binary) AINP = AIN0 and AINN = AIN1, +/- 6.144 V
    # Continuous conversion mode, 128SPS

    data = [0xD0, 0x83]
    bus.write_i2c_block_data(0x48, 0x01, data)
    time.sleep(1)

    # ADS1115 address, 0x48(72)
    # Read data back from 0x00(00), 2 bytes
    # raw_adc MSB, raw_adc LSB
    data = bus.read_i2c_block_data(0x48, 0x00, 2)

    # print(data)
    # Convert the data
    raw_adc = data[0] * 256 + data[1]

    # if raw_adc > 32767:
    # 	raw_adc -= 65535

    digital_voltage = raw_adc / 32767 * 6.144

    #print("Digital Voltage (V): " + str(digital_voltage))

    return digital_voltage