import subprocess as sp
import threading
import time
import os
import signal


class ffmpegStreamThread(threading.Thread):


    def __init__(self, ip, clientID):

        #ip = '192.168.1.77'
        #clientID = 'picam2'

        self.stdout = None
        self.stderr = None
        self.ip = ip
        self.clientID = clientID
        threading.Thread.__init__(self)
        self.event = threading.Event()        

    def stopped(self):
        return self.event.isSet()

    def stop(self):
        self.event.set()

    def run(self):
        self.startProcess(self.ip, self.clientID)

    def startProcess(self, ip, clientID):
        FFMPEG_BIN = 'ffmpeg'
        
        command = [
                    FFMPEG_BIN,
                    '-i', 'tcp://127.0.0.1:8181?listen',
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-ar', '44100',
                    '-ab', '40000',
                    '-timeout', '3',
                    '-f', 'flv rtmp://'+ip+'/live/'+clientID 
                  ]

        self.pro = sp.Popen(command, stdout=sp.PIPE, bufsize = 10**8)
        self.stdout, self.stderr = p.communicate()

    def stopProcess(self):
        os.killpg(os.getpgid(self.pro.pid),signal.SIGTERM)
