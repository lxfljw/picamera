#!/usr/bin/env python

import threading
import RPi.GPIO as GPIO
import json
import os


class pinsThread(threading.Thread):
    # setup the thread object
    def __init__(self, settingsFilePath, settings):
        threading.Thread.__init__(self)

        self.settingsFilePath = settingsFilePath

        GPIO.cleanup() # resets pins
        GPIO.setmode(GPIO.BOARD)

        # load settings
        for key in settings:
            print key, ':', settings[key]

            GPIO.setup(int(key), GPIO.OUT)
            GPIO.output(int(key), settings[key])

    def update_pin(self, pin, value):
        GPIO.output(pin, value)
        print "updated pin " + str(pin) + " to" + str(value)

        # save pin to file
        data = None
        with open(self.settingsFilePath, 'r+') as data_file:
            data = json.load(data_file)
            data["pin_settings"][str(pin)] = value

            data_file.seek(0)
            json.dump(data, data_file, indent=2)
            data_file.truncate() # clear out the file before saving
