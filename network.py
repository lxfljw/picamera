#!/usr/bin/env python

import threading
import os
import paho.mqtt.client as mqtt
import json

import socket
import fcntl
import struct

import time
from threading import Timer

import logging

import base64
import random, string
import math



def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


class mqttThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, mqttObject, fallbackLoopTime, cameraThread):
        threading.Thread.__init__(self)

        # setup thread variables

        print '............',mqttObject['clientID'],  mqttObject['brokerURL'],mqttObject['brokerPort']
        
        self.clientID = mqttObject['clientID']
        self.brokerURL = mqttObject['brokerURL']
        self.brokerPort = mqttObject['brokerPort']
        self.captureTopic = str(mqttObject['publish']['captureTopic'])
        self.rebootTopic = str(mqttObject['publish']['rebootTopic'])
        self.settingsTopic = str(mqttObject['publish']['settingsTopic'])
        self.startCaptureTopic = str(mqttObject['publish']['startCaptureTopic'])
        self.stopCaptureTopic = str(mqttObject['publish']['stopCaptureTopic'])
        self.startStreamTopic = str(mqttObject['publish']['startStreamTopic'])
        self.stopStreamTopic = str(mqttObject['publish']['stopStreamTopic'])

        self.statusTopic = str(mqttObject['subscribe']['statusTopic'])
        
        #self.pinsTopic = str(pinsTopic)
        self.fallbackLoopTime = fallbackLoopTime
        self.cameraThread = cameraThread
        #self.pinsThread = pinsThread

        #self.cameraThread.update_annotation("Camera " + self.clientID + " Connecting...", "blue")
        
        self.client = mqtt.Client(client_id=self.clientID, clean_session=True)
        self.client.will_set(self.statusTopic, json.dumps({'status':0}))

        self.cameraThread.start()
        

    def reboot(self):
        logging.info("reboot...")
        try:
            self.client.publish("debug", self.clientID + " reboot...")
            #os.system("sudo shutdown -h now")
            os.system("sudo reboot")
        except Exception as e:
            logging.error("reboot exception "+ time.time())

    def capture(self):
        print('capture ')       
        logging.info( "capturing image ")
        try:
            self.cameraThread.capture()
        except Exception as e:
            logging.error("capture exception ")

    def startCaptureTopic(self):
        #logging.info("self.cameraThread.enable() ")
        try:
            self.cameraThread.enable()
        except Exception as e:
            logging.error("startCaptureTopic exception ")

    def stopCaptureTopic(self):
        print("stopCaptureTopic ") 
        logging.info("stopCaptureTopic...")
        try:
            self.cameraThread.disable()
        except Exception as e:
            logging.error("stopCaptureTopic exception ")
        

    def startStreamTopic(self):
        logging.info("startStreamTopic...")
        try:
            print "startStreamTopic "
        except Exception as e:
            logging.error("startStreamTopic exception ")
        
    def stopStreamTopic(self):
        print('stopStreamTopic ')            
        logging.info('stopStreamTopic...')
        try:
            print 'stopStreamTopic '              
        except Exception as e:
            logging.error("stopStreamTopic exception ")        

    def update_setting(self, payload):
        settings = json.loads(payload)
        self.client.publish("debug", self.clientID + " updating " + str(settings["setting"])+ " "+str(settings["value"]))
        self.cameraThread.update_setting(settings["setting"],settings["value"])
        self.client.publish("debug", self.clientID + " updated " + str(settings["setting"])+ " "+str(settings["value"]))

    def update_pin(self, payload):
        settings = json.loads(payload)
        self.client.publish("debug", self.clientID + " updating pin " + str(settings["pin"])+ " "+str(settings["value"]))
        #self.pinsThread.update_pin(settings["pin"],settings["value"])
        self.client.publish("debug", self.clientID + " updated pin " + str(settings["pin"])+ " "+str(settings["value"]))

    def on_message(self, client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
        logging.info("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))


        if message.topic == self.captureTopic:
            self.capture()
        elif message.topic == self.rebootTopic:
            self.reboot()
        elif message.topic == self.settingsTopic:
            self.update_setting(message.payload)
            
        elif message.topic == self.startCaptureTopic:
            #self.startCaptureTopic()
            try:
                self.cameraThread.enable()
            except Exception as e:
                logging.error("startCaptureTopic exception "+ str(e))           
        elif message.topic == self.stopCaptureTopic:
            #self.stopCaptureTopic()
            try:
                self.cameraThread.disable()
            except Exception as e:
                logging.error("stopCaptureTopic exception "+ str(e))              
        elif message.topic == self.startStreamTopic:
            self.startStreamTopic()
            
        elif message.topic == self.stopStreamTopic:
            self.stopStreamTopic()
            
        #elif message.topic == self.pinsTopic:
        #    self.update_pin(message.payload)

    def on_connect(self, client, userdata, flags, rc):
        print("Connection connected " + str(rc))
        logging.info("Connection connected " + str(rc))
        #self.capture()
        self.client.publish(self.statusTopic, json.dumps({'status':1}) )
 
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
            logging.info("Unexpected MQTT disconnection. Will auto-reconnect" + str(rc))


    def fallback(self):
        while True:
            #self.cameraThread.update_annotation("Camera " + self.clientID + " Fallback Mode: " + str(self.fallbackLoopTime) + "secs", "red")
            self.capture()
            time.sleep(self.fallbackLoopTime)
            print("taking image")

    def run(self):
        self.client.on_connect = self.on_connect

        print self.brokerURL
        try:
            print self.brokerURL, self.brokerPort
            self.client.connect(self.brokerURL, self.brokerPort, 60)

            self.client.subscribe(self.captureTopic, qos=0)
            self.client.subscribe(self.rebootTopic, qos=0)
            self.client.subscribe(self.settingsTopic, qos=0)
            self.client.subscribe(self.startCaptureTopic, qos=0)
            self.client.subscribe(self.stopCaptureTopic, qos=0)
            self.client.subscribe(self.startStreamTopic, qos=0)
            self.client.subscribe(self.stopStreamTopic, qos=0)
            #self.client.subscribe(self.pinsTopic, qos=0)

            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect


            self.client.publish("debug", self.clientID + " connected IP:")  # + get_ip_address('eth0')
            #self.cameraThread.update_annotation("Camera " + self.clientID, "green")
            self.client.loop_forever()
        except socket.gaierror:
            print "No Connection"
            #self.fallback()



    #  mqtt message 
    #  https://developer.ibm.com/recipes/tutorials/sending-and-receiving-pictures-from-a-raspberry-pi-via-mqtt/
    #  http://stackoverflow.com/questions/36429609/mqtt-paho-python-reliable-reconnect
    def convertImageToBase64():
        with open(self.filePath + '/test.jpg', "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            return encoded


    def randomword(length):
        return ''.join(random.choice(string.lowercase) for i in range(length)) 


    def publishEncodedImage(encoded):
        
        packet_size=3000

        end = packet_size
        start = 0
        length = len(encoded)
        picId = randomword(8)
        pos = 0
        no_of_packets = math.ceil(length/packet_size)

         
        while start <= len(encoded):
            data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets}
            self.client.publish("Image-Data",json.JSONEncoder().encode(data))
            end += packet_size
            start += packet_size
            pos = pos +1        
