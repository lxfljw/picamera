#!/bin/sh

echo Starting....

sudo apt-get update
#!sudo apt-get upgrade -y

cat system-requirements.txt | xargs sudo apt-get install -y

sudo pip install -r python-requirements.txt

sudo cp camera.conf /etc/supervisor/conf.d/
sudo cp backup.conf /etc/supervisor/conf.d/

sudo supervisorctl reload

sudo mkdir /media/usb
sudo mkdir /media/nas

sudo reboot
