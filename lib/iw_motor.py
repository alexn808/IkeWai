# This program will make one stepper motor spin with speed controls.

import RPi.GPIO as GPIO
import time

# Variables

# Choose a delay between 0.0055 and greater
delay = 0.0055
#steps = 100

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Enable GPIO pins for  ENA and ENB for stepper
enable_a = 18
enable_b = 12
enable = 5

# Enable pins for IN1-4 to control step sequence
coil_A_1_pin = 24
coil_A_2_pin = 23
coil_B_1_pin = 22
coil_B_2_pin = 27

# Set pin states

GPIO.setup(enable, GPIO.OUT)
GPIO.setup(enable_a, GPIO.OUT)
GPIO.setup(enable_b, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Set ENA and ENB to high to enable stepper
GPIO.output(enable, True)
GPIO.output(enable_a, True)
GPIO.output(enable_b, True)


# Function for step sequence
# Motor pinout for regular execution.
# motorA on chip is blue outside, yellow inside
# motorB on chip is green outside, red inside

# Motor pinout for soldered execution.
# motorA on chip is blue outside, yellow inside
# motorB on chip is red outside, green inside

# yellow, blue, red, green
def set_step(w1, w2, w3, w4):
    # Sequence for soldered execution.
    GPIO.output(coil_A_1_pin, w1)  # Outside motorA (blue)
    GPIO.output(coil_A_2_pin, w2)  # Inside motorA (yellow)
    GPIO.output(coil_B_1_pin, w4)  # Outside motorB (red)
    GPIO.output(coil_B_2_pin, w3)  # Inside motorB (green)


    # Sequence for regular execution.
    # GPIO.output(coil_A_1_pin, w1)
    # GPIO.output(coil_A_2_pin, w2)
    # GPIO.output(coil_B_1_pin, w3)
    # GPIO.output(coil_B_2_pin, w4)

# loop through step sequence based on number of steps

#clockwise when facing the nonshaft side of motor
# for i in range(0, steps):
# 	setStep(1,0,1,0)
# 	time.sleep(delay)
# 	setStep(0,1,1,0)
# 	time.sleep(delay)
# 	setStep(0,1,0,1)
# 	time.sleep(delay)
# 	setStep(1,0,0,1)
# 	time.sleep(delay)

# Reverse previous step sequence to reverse motor direction
#setStep(0,0,0,0)
#time.sleep(1)
#counterclockwise when facing nonshaft side of motor


def raise_sensors(steps):
    for i in range(0, steps):
        set_step(1, 0, 0, 1)
        time.sleep(delay)
        set_step(0, 1, 0, 1)
        time.sleep(delay)
        set_step(0, 1, 1, 0)
        time.sleep(delay)
        set_step(1, 0, 1, 0)
        time.sleep(delay)

    # Cut power to motor.
    #set_step(0, 0, 0, 0)

    # Hold motor position.
    # setStep(1,0,1,0)


def lower_sensors(steps):
    for i in range(0, steps):
        set_step(1,0,1,0)
        time.sleep(delay)
        set_step(0,1,1,0)
        time.sleep(delay)
        set_step(0,1,0,1)
        time.sleep(delay)
        set_step(1,0,0,1)
        time.sleep(delay)

    # Cut power to motor.
    #set_step(0, 0, 0, 0)
