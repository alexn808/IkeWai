# This program will make one stepper motor spin with speed controls.

import RPi.GPIO as GPIO
import time

# Variables

# Choose a delay between 0.0055 and greater
delay = 0.0055
steps = 500

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


#yellow, blue, red, green
def set_step(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

# loop through step sequence based on number of steps

# print("starting spin...")

# 50% duty cycle

#clockwise when facing the nonshaft side of motor
# for i in range(0, steps):
#     setStep(1,0,1,0)
#     time.sleep(delay)
#     setStep(0,1,1,0)
#     time.sleep(delay)
#     setStep(0,1,0,1)
#     time.sleep(delay)
#     setStep(1,0,0,1)
#     time.sleep(delay)

# Reverse previous step sequence to reverse motor direction
#setStep(0,0,0,0)
#time.sleep(1)
#counterclockwise when facing nonshaft side of motor


while True:
	for i in range(0, steps):
		set_step(1, 0, 0, 1)
		time.sleep(delay)
		set_step(0, 1, 0, 1)
		time.sleep(delay)
		set_step(0, 1, 1, 0)
		time.sleep(delay)
		set_step(1, 0, 1, 0)
		time.sleep(delay)

# # Cut power to motor.
# set_step(0, 0, 0, 0)
# time.sleep(5)

# Hold motor position.
#setStep(1,0,1,0)
