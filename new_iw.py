import time
import datetime
import logging
import json
import os
import socket

import lib.iw_motor
import lib.iw_adc
import lib.iw_acc
import lib.iw_hot
import lib.iw_rgb


# Defining all the read functions for sensors

def log_iw(message):
    print(message)
    logging.debug(message)


def read_adc0():
    adc_voltage0 = lib.iw_adc.get_adc0()
    log_iw("A0 (V): " + str(adc_voltage0))
    return adc_voltage0


def read_adc1():
    adc_voltage1 = lib.iw_adc.get_adc1()
    log_iw("A1 (V): " + str(adc_voltage1))
    return adc_voltage1


def read_rgb_initial():
    lib.iw_rgb.get_rgb()


def read_rgb():
    lib.iw_rgb.turn_led_on()
    time.sleep(1)
    rgb_values = lib.iw_rgb.get_rgb()
    log_iw("Red:     " + str(rgb_values[0]))
    log_iw("Green:   " + str(rgb_values[1]))
    log_iw("Blue:    " + str(rgb_values[2]))
    lib.iw_rgb.turn_led_off()
    return rgb_values


def read_acc():
    acc = lib.iw_acc.get_acc()
    log_iw("X-Acc:   " + str(acc[0]))
    log_iw("Y-Acc:   " + str(acc[1]))
    log_iw("Z-Acc:   " + str(acc[2]))
    return acc


def read_hot():
    hot = lib.iw_hot.get_hot()
    log_iw("Temp (C):    " + str(hot[0]))
    log_iw("Temp (F):    " + str(hot[1]))
    return hot


# Determine which sensor failed during the 10-sample collection.
def get_bad_sensor(y_value):
    switcher = {
        0: 'ADC0 failed...',
        1: 'ADC1 failed...',
        2: 'RGB failed...',
        3: 'ACC failed...',
        4: 'HOT failed...',
    }

    # Returns the current index of read_array being run.
    return switcher.get(y_value, "nothing")


read_array = [read_adc0, read_adc1, read_rgb, read_acc, read_hot]
total_steps = 0
# Change the level_count for how much increments you want to go up
# from the bottom of the well
# The value is how much times it goes up
# ex. 3 = 15 feet up from bottom, 4 = 20 feet up from bottom
level_count = 3
#3600 1 hour
#Time between samples
sleep_between_trials = 3600 # change to 3600 after demo

adc_initial = 0
depth = 0
#steps_for_foot = 125 # Real
steps_for_foot = 125 # demo
steps_for_5_foot = steps_for_foot * 5 # change to 5 after demo


if __name__ == "__main__":

    # print('Starting')
    # print('Spinning')
    # lib.iw_motor.lower_sensors(steps_for_foot)
    # print('Done')

    # print("0001")
    # lib.iw_motor.set_step(0, 0, 0, 1)
    # time.sleep(120)

    # Create empty dictionaries to store each sensor reading
    iw_dict = {}
    iw_dict_adc = {}
    iw_dict_rgb = {}
    iw_dict_acc = {}
    iw_dict_hot = {}

    # Create the empty list to store the the entire data collection
    iw_dict_l = []
    iw_dict_adc_l = []
    iw_dict_rgb_l = []
    iw_dict_acc_l = []
    iw_dict_hot_l = []

    count = 0
    # Dropping the module down for about 60 seconds
    while count != 1:
        lib.iw_motor.set_step(0, 0, 0, 0)
        time.sleep(60)
        count += 1
    while True:
        try:
            # Get the current date and time from computer in format: MMDDYYYY-HHMMSS for log file purposes.
            dt1 = list(str(datetime.datetime.now()))
            dt = dt1
            dt[4] = ''
            dt[7] = ''
            dt[10] = '_'
            dt[13] = ''
            dt[16] = ''
            dt = "".join(dt)
            dt = list(dt)
            dt[0], dt[4] = dt[4], dt[0]
            dt[1], dt[5] = dt[5], dt[1]
            dt[2], dt[6] = dt[6], dt[2]
            dt[3], dt[7] = dt[7], dt[3]
            dt = "".join(dt)

            # Truncate dt to 15 bits, 0 - 14.
            dt = dt[0:15]

            # Rearrange the string to be in HHMMSS-MMDDYYYY
            dt = list(dt)
            dt.insert(0, dt.pop(8))
            dt.insert(0, dt.pop(14))
            dt.insert(0, dt.pop(14))
            dt.insert(0, dt.pop(14))
            dt.insert(0, dt.pop(14))
            dt.insert(0, dt.pop(14))
            dt.insert(0, dt.pop(14))
            dt = "".join(dt)

            # Log files for debug in case of errors
            # Sometimes the log file has errors since the path
            # for the log file is written, you may have to comment this out this section out
            log_name = 'log_' + dt + '.txt'
            logging.basicConfig(filename=r'/home/pi/Desktop/ikewai/logs/client_logs/' + log_name, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            log_iw('iw.py starting...')
            log_iw('Time_Date: ' + str(dt))

            # For some reason, the first read of the RGB sensor returns 0,0,0.
            try:
                read_rgb_initial()
            except IOError:
                log_iw('IOError from initial RGB occurred...')
                pass
            # Drop the module all the way down
            #sampling
            for w in range(0, level_count):
                level_dict = 'Level ' + str(w)
                iw_dict[level_dict] = ''
                iw_dict_l.append(iw_dict)
                log_iw('Level #' + str(w))

                # Read first 10 samples. 0,11
                for x in range(1, 2):
                    log_iw('Level-Sample: ' + str(w) + '-' + str(x))
                    for y in range(0, 5):
                        reading_number = 'R' + str(x)
                        try:
                            # Read sensor values
                            value = read_array[y]()
                            # Each sensor has their owned predefined integer value (0-4)
                            if y == 0:
                                # Assigning the ADC dictionary
                                # variable A0 to have the sensor value
                                iw_dict_adc['A0 ' + reading_number] = value
                                # appending the dictionary reading into a list
                                iw_dict_adc_l.append(iw_dict_adc)
                            elif y == 1:
                                iw_dict_adc['A1 ' + reading_number] = value
                                iw_dict_adc_l.append(iw_dict_adc)
                            elif y == 2:
                                iw_dict_rgb['Red ' + reading_number] = value[0]
                                iw_dict_rgb['Green ' + reading_number] = value[1]
                                iw_dict_rgb['Blue ' + reading_number] = value[2]
                                iw_dict_rgb_l.append(iw_dict_rgb)
                            elif y == 3:
                                iw_dict_acc['X ' + reading_number] = value[0]
                                iw_dict_acc['Y ' + reading_number] = value[1]
                                iw_dict_acc['Z ' + reading_number] = value[2]
                                iw_dict_acc_l.append(iw_dict_acc)
                            elif y == 4:
                                iw_dict_hot['C ' + reading_number] = value[0]
                                iw_dict_hot['F ' + reading_number] = value[1]
                                iw_dict_hot_l.append(iw_dict_hot)
                        # When there is an error (sensor not working)
                        except IOError:
                            log_iw('IOError during 10 occurred...')
                            log_iw(get_bad_sensor(y))
                            if y == 0:
                                iw_dict_adc['A0 ' + reading_number] = get_bad_sensor(y)
                                iw_dict_adc_l.append(iw_dict_adc)
                            elif y == 1:
                                iw_dict_adc['A1 ' + reading_number] = get_bad_sensor(y)
                                iw_dict_adc_l.append(iw_dict_adc)
                            elif y == 2:
                                iw_dict_rgb['Red ' + reading_number] = get_bad_sensor(y)
                                iw_dict_rgb['Green ' + reading_number] = get_bad_sensor(y)
                                iw_dict_rgb['Blue ' + reading_number] = get_bad_sensor(y)
                                iw_dict_rgb_l.append(iw_dict_rgb)
                            elif y == 3:
                                iw_dict_acc['X ' + reading_number] = get_bad_sensor(y)
                                iw_dict_acc['Y ' + reading_number] = get_bad_sensor(y)
                                iw_dict_acc['Z ' + reading_number] = get_bad_sensor(y)
                                iw_dict_acc_l.append(iw_dict_acc)
                            elif y == 4:
                                iw_dict_hot['C ' + reading_number] = get_bad_sensor(y)
                                iw_dict_hot['F ' + reading_number] = get_bad_sensor(y)
                                iw_dict_hot_l.append(iw_dict_hot)
                            pass

                # raise sensor module 5 more feet.
                log_iw('raise sensor module to next increment...')
                lib.iw_motor.raise_sensors(steps_for_5_foot)
                total_steps = total_steps + steps_for_5_foot
                time.sleep(5)
                # Dropping the module down again
            count = 0
            while count != 1:
                lib.iw_motor.set_step(0, 0, 0, 0)
                time.sleep(60)
                count += 1
            log_iw('Sleeping...')
            time.sleep(sleep_between_trials)

        # When someone exits the program
        except(KeyboardInterrupt, SystemExit):
            # Convert python list into json format
            dict_file = json.dumps(iw_dict_l)
            adc_file = json.dumps(iw_dict_adc_l)
            rgb_file = json.dumps(iw_dict_rgb_l)
            acc_file = json.dumps(iw_dict_acc_l)
            hot_file = json.dumps(iw_dict_hot_l)

            # Creating the name of the file
            dict_log = "dict_" + timestamp

            # Creating the directory where we would write the file
            # and giving writing its name
            completeName = os.path.join(save_path, '%s.json' % dict_log)

            # The 'a' appends the file if there is an existing file
            # the '+' creates the file if there isn't an existing file
            f = open(completeName, "a+")

            # Dumping the data from the earlier conversion
            # into the newly created file
            f.write(dict_file)

            # Closing the file
            f.close()

            adc_log = "adc_" + timestamp
            completeName = os.path.join(save_path, '%s.json' % adc_log)
            f = open(completeName, "a+")
            f.write(adc_file)
            f.close()

            rgb_log = "rgb_" + timestamp
            completeName = os.path.join(save_path, '%s.json' % rgb_log)
            f = open(completeName, "a+")
            f.write(rgb_file)
            f.close()

            acc_log = "acc_" + timestamp
            completeName = os.path.join(save_path, '%s.json' % acc_log)
            f = open(completeName, "a+")
            f.write(acc_file)
            f.close()

            hot_log = "hot_" + timestamp
            completeName = os.path.join(save_path, '%s.json' % hot_log)
            f = open(completeName, "a+")
            f.write(hot_file)
            f.close()

            log_iw('Exiting...')
            # Turn off the LED before exiting
            lib.iw_rgb.turn_led_off()
            log_iw('Exited...')
            break
