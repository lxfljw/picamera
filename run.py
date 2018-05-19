from camera import cameraThread
from network import mqttThread
from pins import pinsThread
import time
import json
import os
import logging

# Mount usb drive

#os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")

# load settings from file

settings = None
settingsFilePath = '/home/pi/Desktop/PiCameraClient/settings.json'
loggingFilePath = '/home/pi/Desktop/PiCameraClient/logging.log'

with open(settingsFilePath) as data_file:
    conent = data_file
    settings = json.load(conent)
    print settings['mqtt']['clientID'],settings['mqtt']['brokerURL'],settings['mqtt']['brokerPort'],settings["server"],settings["camera_settings"]


logging.basicConfig(filename=loggingFilePath, level=logging.INFO, format='%(asctime)s;%(levelname)s;%(message)s')

print "-----------------------------------run.py----------------------------"
clientID = settings['mqtt']['clientID']
server_setting = settings["server"]
mqtt_setting = settings['mqtt']

server_setting['url'] = server_setting['url'].replace(':deviceID',clientID)
mqtt_setting['publish']['rebootTopic'] = mqtt_setting['publish']['rebootTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['settingsTopic'] = mqtt_setting['publish']['settingsTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['captureTopic'] = mqtt_setting['publish']['captureTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['startCaptureTopic'] = mqtt_setting['publish']['startCaptureTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['stopCaptureTopic'] = mqtt_setting['publish']['stopCaptureTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['startStreamTopic'] = mqtt_setting['publish']['startStreamTopic'].replace(':deviceID',clientID)
mqtt_setting['publish']['stopStreamTopic'] = mqtt_setting['publish']['stopStreamTopic'].replace(':deviceID',clientID)
print "-----------------------------------run.py1----------------------------"
mqtt_setting['subscribe']['statusTopic'] = mqtt_setting['subscribe']['statusTopic'].replace(':deviceID',clientID)

m = mqttThread(
    mqtt_setting,
    settings["fallbackLoopTime"],
    cameraThread(settings["localImageFolder"], settingsFilePath, settings["camera_settings"], server_setting)
)

m.run()

