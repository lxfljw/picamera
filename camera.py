#!/usr/bin/env python

import threading
import time
import picamera
import json
import os
import datetime
import requests
import logging


class cameraThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, filePath, settingsFilePath, settings, server):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 10
        

        self.filePath = filePath
        self.settingsFilePath = settingsFilePath
        self.interval = server['interval']

        print settings
        print server
        print settings['led']
        print server['url']
        
        self.ip = server['ip']
        self.url = server['url']

        self.enabled = False
        # set up camera
        self.camera = picamera.PiCamera()


        self.camera.annotate_text = ""

        # load settings
        for key in settings:
            print key, ':', settings[key]

            setattr(self.camera, key, settings[key])

    def run(self):
        print 'runing'
        logging.info('running')
        #while self.count > 0 and not self.event.is_set():
        while True:
            #print self.count
            #self.count -=1
            #print self.count
            #if(self.count == 0):
            #    self.count = 10
            #logging.info('run')
            if(self.enabled == True):
                #logging.info('running enabled')
                print 'capture and send image'
                self.capture()
                self.sendImage()
            
            self.event.wait(self.interval)
        print 'stopping'

    def enable(self):
        logging.info('camera enabled')
        self.enabled = True

    def disable(self):
        logging.info('camera disabled')
        self.enabled = False

    def stopped(self):
        return self.event.isSet()

    def stop(self):
        self.event.set()

    def sendImage(self):
        logging.info('sendImage '+'http://'+self.ip+self.url)

        files = {'file':open('/home/pi/Desktop/test.jpg','rb')}
        print 'http://'+self.ip+self.url
        try:
            r = requests.post('http://'+self.ip+self.url, files=files)
        except requests.exceptions.RequestException as e:
            loggin.error( str(e))

    def update_annotation(self, text, color_string):
        self.camera.annotate_text = text
        self.camera.annotate_background = picamera.Color.from_string(color_string)

    def capture(self):

        logging.info('capture')
        
        self.camera.start_preview(fullscreen=False, window=(100,20,640,480))
        self.camera.resolution = (2592, 1944)
        
        # hide text
        text = self.camera.annotate_text
        self.camera.annotate_text = ""

        now = time.time()
        print self.filePath + str(now) + '.jpg', datetime.date.today()
        name = datetime.date.today()
        #self.camera.capture(self.filePath + '/'+str(name) + '.jpg')
        self.camera.capture(self.filePath + '/test.jpg')
        
        self.camera.annotate_text = text
        

    def update_setting(self, setting, value):
        # live update
        print "updating " + setting
        setattr(self.camera, setting, value)

        # save setting to file
        data = None
        with open(self.settingsFilePath, 'r+') as data_file:
            data = json.load(data_file)
            data["camera_settings"][setting] = value

            data_file.seek(0)
            json.dump(data, data_file, indent=2)
            data_file.truncate() # clear out the file before saving
