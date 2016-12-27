import subprocess as sp
import threading
import time
import os
import signal

class picameraThread(threading.Thread):

    def __init__(self):

        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def stopped(self):
        return self.event.isSet()

    def stop(self):
        self.event.set()

    def run(self):
        self.startProcess(self.ip, self.clientID)

    def startProcess(self, ip, clientID):
        PICAM_BIN = './home/pi/Desktop/picam/picam'
        
        command = [
                    PICAM_BIN,
                    '--tcpout', 'tcp://127.0.0.1:8181' 
                  ]

        self.pro = sp.Popen(command, stdout=sp.PIPE, bufsize = 10**8)
        self.stdout, self.stderr = p.communicate()

    def stopProcess(self):
        os.killpg(os.getpgid(self.pro.pid),signal.SIGTERM)
