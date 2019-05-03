# import libraries
import time
import Adafruit_ADS1x15

# create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# set gain to 1 -----> 4.096n
GAIN = 1

# print header
print("   ADC values")
print("  a0   ,   a1  ")

# collect data from ADC and output voltages
while True:

    # read raw values from a0 and a1 inputs
    a0 = float(adc.read_adc(0, gain=GAIN))
    a1 = float(adc.read_adc(1, gain=GAIN))

    # convert raw values to voltages [V]
    voltage_a0 = a0 / 32767 * 4.096
    voltage_a1 = a1 / 32767 * 4.096

    # print voltages
    print("{:.4f}".format(voltage_a0)),
    print(","),
    print("{:.4f}".format(voltage_a1))

    time.sleep(1)
