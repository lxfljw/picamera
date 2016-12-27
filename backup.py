#!/usr/bin/env python

import time
import threading
import os
import json

class backupThread(threading.Thread):
    def __init__(self, backupMountScript, localImageFolder, backupDirectory):
        threading.Thread.__init__(self)

        self.localImageFolder = localImageFolder
        self.backupDirectory = backupDirectory

        print "mounting nas"
        os.system(backupMountScript)

    def start(self):
        #time.sleep(30)
        while True:
            #print "backing up"
            os.system("sudo rsync -a "+self.localImageFolder+" "+self.backupDirectory)
            time.sleep(10)


settings = None

time.sleep(60)

with open('/media/usb/settings.json') as data_file:
    settings = json.load(data_file)

print settings["backupActive"]
if settings["backupActive"]:
    b = backupThread(
        settings["backupMountScript"],
        settings["localImageFolder"],
        settings["backupDirectory"]
    )
    b.start()
else:
    ainput = raw_input("Backup deactivated")
