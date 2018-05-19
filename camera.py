#!/usr/bin/env python

import threading
import time
import picamera
import json
import os
import datetime
import requests
import logging
from termcolor import colored


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
        print "+++++++++++++++++++camera.py+++++++++++++++++"
        self.ip = server['ip']
        self.url = server['url']

        self.enabled = True
        # set up camera
        # self.camera = picamera.PiCamera()
        print (colored('capture 1','red'))
        #self.capture()
#==============================================
        self.vediotape()
        
        # load settings
        for key in settings:
            print key, ':', settings[key]
           
            #setattr(self.camera, key, settings[key])

    def run(self):
        print 'runing......'
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
                print colored('capture and send image'  ,'green')
#===========================================================
               # self.capture()
                #self.sendImage()
                self.vediotape()
                self.sendvedio()
 #===========================================================               
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
        files = {'file':open(self.filePath + '/test.jpg','rb')}
        print colored('http://'+self.ip+self.url,'green')
        print files
        try:
            r = requests.post('http://'+self.ip+self.url, files=files)
        except requests.exceptions.RequestException as e:
            loggin.error( str(e))

#=============================================================
    def sendvedio(self):
        logging.info('sendIvedio '+'http://'+self.ip+self.url)
        files = {'file':open(self.filePath + '/test.h264','rb')}
        print colored('http://'+self.ip+self.url,'green')
        print files
        try:
            r = requests.post('http://'+self.ip+self.url, files=files)
        except requests.exceptions.RequestException as e:
            loggin.error( str(e))
    def update_annotation(self, text, color_string):
        self.camera.annotate_text = text
        self.camera.annotate_background = picamera.Color.from_string(color_string)
#=================================================================
    def vediotape(self):

        logging.info('vediotape')
        print colored("vediotape",'yellow')
        # hide text
        #text = self.camera.annotate_text
        #self.camera.annotate_text = ""



        self.camera = picamera.PiCamera()
        try: 
            self.camera.start_preview()
            time.sleep(1)

           
            #self.camera.capture(self.filePath + '/'+str(name) + '.jpg')
            self.camera.start_recording(self.filePath + '/test.h264')
            self.camera.wait_recording(10)
            self.camera.stop_recording()
            #now = time.time()
            #print self.filePath + str(now) + '.jpg', datetime.date.today()
            #name = datetime.date.today()
            #self.camera.annotate_text = text
            
            pass
        
        finally:
            self.camera.stop_preview()
            self.camera.close()
#=====================================================================
    def capture(self):

        logging.info('capture')
        print colored("capture",'yellow')
        # hide text
        #text = self.camera.annotate_text
        #self.camera.annotate_text = ""



        self.camera = picamera.PiCamera()
        try: 
            self.camera.start_preview(fullscreen=False, window=(100,20,640,480))
            time.sleep(1)

            self.camera.resolution = (2592, 1944)
            #self.camera.capture(self.filePath + '/'+str(name) + '.jpg')
            self.camera.capture(self.filePath + '/test.jpg')
            

            #now = time.time()
            #print self.filePath + str(now) + '.jpg', datetime.date.today()
            #name = datetime.date.today()
            #self.camera.annotate_text = text
            
            pass
        
        finally:
            self.camera.stop_preview()
            self.camera.close()
            
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
