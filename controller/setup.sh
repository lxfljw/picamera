#!/bin/sh

echo Starting....

sudo apt-get update
sudo apt-get upgrade -y

cat system-requirements.txt | xargs sudo apt-get install -y

sudo pip install -r python-requirements.txt

sudo cp server.conf /etc/supervisor/conf.d/

sudo supervisorctl reload

sudo reboot
